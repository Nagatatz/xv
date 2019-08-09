from django.db import models
from django.utils import timezone

from enum import Enum

from common.models import BaseModel, BaseManager
from master.models import (
    PlayerPosition,
    StaffPosition,
    MatchType,
    MatchSwitchEventType,
    ScoringMethod,
    FoulMethod,
)
from member.models import TeamGroup, Member


class HeldManager(BaseManager):

    use_for_related_fields = True

    def held(self, **kwargs):
        return self.filter(held_datetime__lte=timezone.now(), **kwargs)


class TeamOnMatch(BaseModel):
    """
    試合参加チーム
    """

    name = models.CharField(max_length=35, verbose_name='チーム名')
    team_group = models.ForeignKey(
        TeamGroup, null=True, on_delete=models.SET_NULL, verbose_name='チームグループ'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = '試合参加チーム'
        db_table = 'rugby_team_on_match'


class FieldStaff(BaseModel):
    """
    フィールドスタッフ
    """

    name = models.CharField(max_length=35, verbose_name='フィールドスタッフ職')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'フィールドスタッフ'
        db_table = 'rugby_field_staff'


class StaffOnMatch(BaseModel):
    """
    試合参加スタッフ
    """

    team = models.ForeignKey(
        TeamOnMatch, on_delete=models.CASCADE, verbose_name='所属チーム'
    )
    field_staff = models.ForeignKey(
        FieldStaff, on_delete=models.PROTECT, verbose_name='フィールドスタッフ職'
    )
    member = models.ForeignKey(Member, on_delete=models.PROTECT, verbose_name='メンバー')

    class Meta:
        verbose_name_plural = '試合参加スタッフ'
        unique_together = ('team', 'member')
        db_table = 'rugby_staff_on_match'


class PlayerOnMatch(BaseModel):
    """
    試合登録プレイヤー
    """

    team = models.ForeignKey(
        TeamOnMatch, on_delete=models.CASCADE, verbose_name='所属チーム'
    )
    position_number = models.PositiveIntegerField(verbose_name='背番号')
    member = models.ForeignKey(Member, on_delete=models.PROTECT, verbose_name='メンバー')

    class Meta:
        verbose_name_plural = '試合登録プレイヤー'
        unique_together = (('team', 'position_number'), ('team', 'member'))
        db_table = 'rugby_player_on_match'


class Match(BaseModel):
    """
    試合
    """

    held_datetime = models.DateTimeField()
    match_type = models.ForeignKey(
        MatchType, on_delete=models.PROTECT, verbose_name='試合種別'
    )
    referee = models.ForeignKey(
        Member,
        on_delete=models.PROTECT,
        verbose_name='レフリー',
        related_name='match_referee',
    )
    assistant_referee = models.ManyToManyField(
        Member, verbose_name='アシスタントレフリー', related_name='match_assistant_referee'
    )
    touch_judge = models.ManyToManyField(
        Member, verbose_name='タッチジャッジ', related_name='match_touch_judge'
    )
    left_team = models.ForeignKey(
        TeamOnMatch,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='左チーム',
        related_name='match_left',
    )
    right_team = models.ForeignKey(
        TeamOnMatch,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='右チーム',
        related_name='match_right',
    )

    objects = HeldManager()
    all_objects = HeldManager(alive_only=False)

    def __str__(self):
        return f'{self.held_datetime} {self.match_type}'

    class Meta:
        verbose_name_plural = '試合'
        db_table = 'rugby_match'


class Half(BaseModel):
    """
    ハーフ
    """

    match = models.ForeignKey(Match, on_delete=models.CASCADE, verbose_name='試合')
    duration = models.DurationField(verbose_name='時間')
    number = models.IntegerField(verbose_name='序数')

    class Meta:
        verbose_name_plural = 'ハーフ'
        unique_together = ('match', 'number')
        db_table = 'rugby_half'


class MatchEvent(BaseModel):
    """
    試合イベント
    """

    half = models.ForeignKey(Half, on_delete=models.PROTECT, verbose_name='ハーフ')
    duration = models.DurationField(verbose_name='経過時間')

    class Meta:
        verbose_name_plural = '試合イベント'
        abstract = True
        db_table = 'rugby_match_event'


class PatternType(MatchEvent):
    """
    試合イベントパターン
    """

    name = models.CharField(max_length=35, verbose_name='イベント名')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = '試合イベントパターン'
        db_table = 'rugby_pattern_type'


class MatchPatternedEvent(MatchEvent):
    """
    通常試合イベント
    """

    event_type = models.ForeignKey(
        PatternType, on_delete=models.PROTECT, verbose_name='試合中交替/入替イベント種別'
    )

    class Meta:
        verbose_name_plural = '通常試合イベント'
        db_table = 'rugby_match_patterned_event'


class MatchSwitchEvent(MatchEvent):
    """
    試合中交替/入替イベント
    """

    event_type = models.ForeignKey(
        MatchSwitchEventType, on_delete=models.PROTECT, verbose_name='試合中交替/入替イベント種別'
    )
    out_member = models.ForeignKey(
        PlayerOnMatch,
        on_delete=models.PROTECT,
        null=True,
        verbose_name='退場メンバー',
        related_name='match_out',
    )
    in_member = models.ForeignKey(
        PlayerOnMatch,
        on_delete=models.PROTECT,
        null=True,
        verbose_name='出場メンバー',
        related_name='match_in',
    )

    class Meta:
        verbose_name_plural = '試合中交替/入替イベント'
        db_table = 'rugby_match_switch_event'


class MatchScoringEvent(MatchEvent):
    """
    試合中得点イベント
    """

    method = models.ForeignKey(
        ScoringMethod, on_delete=models.PROTECT, verbose_name='得点手法'
    )
    player = models.ForeignKey(
        PlayerOnMatch, on_delete=models.PROTECT, verbose_name='得点メンバー'
    )
    is_no_kick = models.BooleanField(verbose_name='キック蹴らず')

    class Meta:
        verbose_name_plural = '試合中得点イベント'
        db_table = 'rugby_match_scoring_event'


class MatchFoulEvent(MatchEvent):
    """
    試合中反則イベント
    """

    class CARD(Enum):
        safe = ('safe', 'No Card')
        yellow = ('yellow', 'Yellow Card')
        red = ('red', 'Red Card')

        @classmethod
        def get_value(cls, member):
            return cls[member].value[0]

    method = models.ForeignKey(
        FoulMethod, on_delete=models.PROTECT, verbose_name='反則手法'
    )
    player = models.ForeignKey(
        PlayerOnMatch, on_delete=models.PROTECT, verbose_name='反則メンバー'
    )
    card_choice = models.CharField(max_length=6, choices=[x.value for x in CARD])
    out_event = models.ForeignKey(
        MatchSwitchEvent, on_delete=models.PROTECT, null=True, verbose_name='退場イベント'
    )
    penalty_try = models.ForeignKey(
        MatchScoringEvent,
        on_delete=models.PROTECT,
        null=True,
        verbose_name='ペナルティトライイベント',
    )

    class Meta:
        verbose_name_plural = '試合中反則イベント'
        db_table = 'rugby_match_foul_event'
