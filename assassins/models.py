from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from encrypted_fields import EncryptedEmailField, EncryptedCharField
from django.utils import timezone
from datetime import timedelta


class UserManager(BaseUserManager):
    def create_user(self, username, email, first_name, last_name, password=None):
        if not username:
            raise ValueError('The given username must be set')
        if not email:
            raise ValueError('Email must be set')
        if not first_name:
            raise ValueError('First name must be set')
        if not last_name:
            raise ValueError('Last name must be set')

        user = self.model(username=username, email=email, first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, first_name, last_name, password):
        if not password:
            raise ValueError('The password must be set')

        user = self.create_user(username, email, first_name, last_name, password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    """Assassins user"""
    username = models.CharField(max_length=40, unique=True, blank=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    email = EncryptedEmailField()
    first_name = EncryptedCharField(max_length=40)
    last_name = EncryptedCharField(max_length=40)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    def get_full_name(self):
        return self.first_name + ' ' + self.last_name

    def get_short_name(self):
        return self.first_name

    def __unicode__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class GameRules(models.Model):
    """Defines game rules"""
    name = models.CharField(max_length=100, blank=False,
        help_text='Display name')
    max_assigned_targets = models.PositiveSmallIntegerField(default=0,
        help_text='Maximum number of assigned targets (0 => no assigned targets)')
    assign_targets_in_own_faction = models.BooleanField(default=False,
        help_text='Whether a player can have assigned targets in their own faction')
    expiry_days = models.PositiveSmallIntegerField(default=0,
        help_text='Number of days after start when the game automatically ends (0 => no time limit)')

    class Meta:
        verbose_name_plural = 'Game rules'

    def __unicode__(self):
        return self.name


class Faction(models.Model):
    """Faction that game players are loyal to"""
    rules = models.ForeignKey(GameRules, related_name='factions')
    name = models.CharField(max_length=100, blank=False,
        help_text='Display name')
    max_assigned_targets = models.PositiveSmallIntegerField(default=0,
        help_text='Maximum number of targets a player can be assigned from this faction')
    min_starting_players = models.PositiveSmallIntegerField(default=0,
        help_text='Minimum number of players loyal to this faction at the start of the game')
    max_starting_players = models.PositiveSmallIntegerField(default=0,
        help_text='Maximum number of players loyal to this faction at the start of the game (0 => no maximum)')

    def __unicode__(self):
        return '%s in %s' % (self.name, self.rules.name)


class Game(models.Model):
    """Game session"""
    name = models.CharField(max_length=100, blank=False,
        help_text='Display name')
    rules = models.ForeignKey(GameRules)
    start_time = models.DateTimeField(
        help_text='When the game starts')
    end_time = models.DateTimeField(null=True, blank=True, default=None,
        help_text='When the game ends')

    def __unicode__(self):
        return self.name


class Player(models.Model):
    """Player in a game session"""
    user = models.ForeignKey(User, related_name='players')
    faction = models.ForeignKey(Faction, related_name='players')
    game = models.ForeignKey(Game, related_name='players')
    pseudonym = models.CharField(max_length=100, blank=False,
        help_text="Pseudonym used for this game in place of the user's real name")
    score = models.IntegerField(default=0,
        help_text='Current score (higher is better)')
    is_real_name_public = models.BooleanField(default=False,
        help_text="Whether the player's real name is public information")
    is_legal_target_for_all_players = models.BooleanField(default=False,
        help_text='Whether the player is a legal target for all other players')
    life_token = EncryptedCharField(max_length=25, blank=True, default='',
        help_text='Token indicating the player is alive')
    life_token_start_time = models.DateTimeField(null=True, blank=True, default=None,
        help_text='When the life token becomes usable (blank => usable immediately)')
    life_token_end_time = models.DateTimeField(null=True, blank=True, default=None,
        help_text='When the life token expires (blank => until end of game)')

    def __unicode__(self):
        return '%s in %s' % (self.pseudonym, self.game.name)


class GameWinner(models.Model):
    """Winner of a game session"""
    game = models.OneToOneField(Game, related_name='winner')
    player = models.ForeignKey(Player, null=True,
        help_text='Player who won the game')
    faction = models.ForeignKey(Faction, null=True,
        help_text='Faction who won the game')

    def __unicode__(self):
        return u'Winner of %s' % (self.game.name,)


KILL_ROLE_CHOICES = (
    ('K', 'Killer'),
    ('V', 'Victim'),
)


KILL_GAME_CONDITION_CHOICES = (
    ('', 'None'),
    ('P', 'All other players eliminated'),
    ('F', 'All other factions eliminated'),
)


class KillAction(models.Model):
    """Actions that execute when one player kills another"""
    rules = models.ForeignKey(GameRules, related_name='%(class)s_kill_actions')
    killer_faction = models.ForeignKey(Faction, related_name='%(class)s_as_killer')
    victim_faction = models.ForeignKey(Faction, related_name='%(class)s_as_victim')
    is_legal_target = models.BooleanField(
        help_text='Whether the victim was a legal target for the killer')
    game_condition = models.CharField(choices=KILL_GAME_CONDITION_CHOICES, default='', max_length=1, blank=True,
        help_text='Game condition')

    class Meta:
        abstract = True

    def apply(self, killer, victim, killer_score, victim_score):
        """
        Apply the action
        :param killer: player who killed the victim
        :param victim: player who was killed
        :param killer_score: the score of the killer at the time of the kill
        :param victim_score: the score of the victim at the time of the kill
        """
        raise NotImplementedError()

    @property
    def precondition_list(self):
        """List of preconditons for this action"""
        conditions = []

        if self.rules.factions.count() > 1:
            conditions.append('player loyal to %s kills player loyal to %s' % (
                self.killer_faction.name,
                self.victim_faction.name,
            ))

        if self.rules.max_assigned_targets > 0:
            conditions.append('the victim %s an assigned target' % (
                'is' if self.is_legal_target else 'is not',
            ))

        if self.game_condition == '':
            pass
        elif self.game_condition == 'P':
            conditions.append('no other players remain alive')
        elif self.game_condition == 'F':
            conditions.append('all other factions have been eliminated')

        return conditions

    @property
    def precondition_text(self):
        """Text describing preconditions of this action"""
        return ', and '.join(self.precondition_list)

    @property
    def postcondition_list(self):
        """List of postconditions for this action"""
        raise NotImplementedError()

    @property
    def postcondition_text(self):
        """Text describing postconditions of this action"""
        return ', and '.join(self.postcondition_list)

    def __unicode__(self):
        return 'If %s, then %s' % (
            self.precondition_text,
            self.postcondition_text
        )

    @classmethod
    def find_subclass_objects(cls, **kwargs):
        """Find all subclass objects matching a query"""
        objects = []
        for klass in cls.__subclasses__():
            objects.extend(klass.objects.filter(**kwargs))
        return objects

class DestroyLifeTokenKillAction(KillAction):
    """Destroy life token of one of the players"""
    role = models.CharField(choices=KILL_ROLE_CHOICES, max_length=1)
    respawn_hours = models.PositiveSmallIntegerField(default=0,
        help_text='The player respawns in N hours (0 => no respawn)')
    respawn_expiry_hours = models.PositiveIntegerField(default=0,
        help_text='Respawn life token expires N hours after becoming active')

    class Meta:
        verbose_name = 'Destroy life token'
        verbose_name_plural = 'Destroy life token actions'

    def apply(self, killer, victim, killer_score, victim_score):
        player = killer if self.role == 'K' else victim
        player.life_token = ''

        if self.respawn_hours > 0:
            #TODO: get kill time
            kill_time = timezone.now()
            #TODO: generate new life token
            player.life_token = 'abc'
            player.life_token_start_time = kill_time + timedelta(hours=self.respawn_hours)

            if self.respawn_expiry_hours > 0:
                player.life_token_end_time = player.life_token_start_time + timedelta(hours=self.respawn_expiry_hours)
            else:
                player.life_token_end_time = None

        player.save()


    @property
    def postcondition_list(self):
        role_name = 'the killer' if self.role == 'K' else 'the victim'
        conditions = [
            "Destroy %s's Life Token (%s is now dead)" % (role_name, role_name)
        ]

        if self.respawn_hours > 0:
            conditions.append('Issue a new Life Token to %s that will be active in %d hours (respawn)' % (role_name, self.respawn_hours))

        return conditions


class AwardFixedPointsKillAction(KillAction):
    """Award a fixed number of points to one of the players"""
    role = models.CharField(choices=KILL_ROLE_CHOICES, max_length=1)
    points = models.IntegerField()

    class Meta:
        verbose_name = 'Award fixed points'
        verbose_name_plural = 'Award fixed points actions'

    def apply(self, killer, victim, killer_score, victim_score):
        player = killer if self.role == 'K' else victim
        player.score += self.points
        player.save()

    @property
    def postcondition_list(self):
        return ["Add %d %s to %s's score" % (
            self.points,
            'point' if self.points == 1 else 'points',
            'the killer' if self.role == 'K' else 'the victim'
        )]


class ChangeFactionKillAction(KillAction):
    """Change faction of one of the players"""
    role = models.CharField(choices=KILL_ROLE_CHOICES, max_length=1)
    faction = models.ForeignKey(Faction)

    class Meta:
        verbose_name = 'Change faction'
        verbose_name_plural = 'Change faction actions'

    def apply(self, killer, victim, killer_score, victim_score):
        player = killer if self.role == 'K' else victim
        player.faction = self.faction
        player.save()

    @property
    def postcondition_list(self):
        return ["Change %s's loyalty to %s" % (
            'the killer' if self.role == 'K' else 'the victim',
            self.faction.name,
        )]


class DeclareKillerTheWinnerKillAction(KillAction):
    """Declare the killer the winner if all other players are eliminated"""

    class Meta:
        verbose_name = 'Declare killer the winner'
        verbose_name_plural = 'Declare killer the winner actions'

    def apply(self, killer, victim, killer_score, victim_score):
        winner, created = GameWinner.objects.get_or_create(game=killer.game)
        winner.player = killer
        winner.save()

    @property
    def postcondition_list(self):
        return ['Declare the killer the winner of the game']


class DeclareKillersFactionTheWinnerKillAction(KillAction):
    """Declare the killer's faction the winner if all other factions are eliminated"""

    class Meta:
        verbose_name = 'Declare faction the winner'
        verbose_name_plural = 'Declare faction the winner actions'

    def apply(self, killer, victim, killer_score, victim_score):
        winner, created = GameWinner.objects.get_or_create(game=killer.game)
        winner.faction = killer.faction
        winner.save()

    @property
    def postcondition_list(self):
        return ['Declare %s the winner of the game' % (
            self.killer_faction.name,
        )]


class DeclareHighestScoringPlayerTheWinnerKillAction(KillAction):
    """Declare the highest scoring player the winner if all other players are eliminated"""

    class Meta:
        verbose_name = 'Declare highest player the winnner'
        verbose_name_plural = 'Declare highest player the winner actions'

    def apply(self, killer, victim, killer_score, victim_score):
        winner, created = GameWinner.objects.get_or_create(game=killer.game)
        highest_player = killer.game.players.order_by('-score').first()
        winner.player = highest_player
        winner.save()

    @property
    def postcondition_list(self):
        return ['Declare the player with the highest score the winner of the game']