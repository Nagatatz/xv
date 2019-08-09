from django.db import models


from common.models import BaseModel
from master.models import PlayerPosition, StaffPosition


class TeamGroup(BaseModel):
    """
    チームグループ
    """

    name = models.CharField(max_length=35, verbose_name='チームグループ名')
    is_my_team = models.BooleanField(verbose_name='自チームグループか')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'チームグループ'
        db_table = 'rugby_team_group'


class Team(BaseModel):
    """
    チーム
    """

    name = models.CharField(max_length=35, verbose_name='チーム名')
    team_group = models.ForeignKey(
        TeamGroup, on_delete=models.PROTECT, verbose_name='チームグループ'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'チーム'
        db_table = 'rugby_team'


class PlayerProfile(BaseModel):
    """
    選手プロフィール
    """

    height = models.DecimalField(verbose_name='身長', max_digits=4, decimal_places=1)
    weight = models.DecimalField(verbose_name='体重', max_digits=4, decimal_places=1)
    player_position = models.ManyToManyField(PlayerPosition, 'ポジション')

    class Meta:
        verbose_name_plural = '選手プロフィール'
        db_table = 'rugby_player_profile'


class Member(BaseModel):
    """
    チーム人員
    """

    family_name = models.CharField(max_length=35, verbose_name='姓')
    first_name = models.CharField(max_length=35, verbose_name='名')
    birthday = models.DateField(null=True, verbose_name='誕生日')
    in_our_team = models.Field()
    player_profile = models.OneToOneField(
        PlayerProfile, on_delete=models.CASCADE, null=True, verbose_name='選手プロフィール'
    )
    staff_position = models.ManyToManyField(StaffPosition, '役職')

    def __str__(self):
        return f'{self.family_name} {self.first_name}'

    class Meta:
        verbose_name_plural = 'チーム人員'
        db_table = 'rugby_member'
