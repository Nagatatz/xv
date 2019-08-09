# Generated by Django 2.2 on 2019-08-09 16:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [('master', '0001_initial'), ('member', '0001_initial')]

    operations = [
        migrations.CreateModel(
            name='FieldStaff',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'created_at',
                    models.DateTimeField(auto_now_add=True, verbose_name='作成日時'),
                ),
                (
                    'updated_at',
                    models.DateTimeField(auto_now=True, verbose_name='更新日時'),
                ),
                (
                    'deleted_at',
                    models.DateTimeField(blank=True, null=True, verbose_name='削除日時'),
                ),
                ('name', models.CharField(max_length=35, verbose_name='フィールドスタッフ職')),
            ],
            options={
                'verbose_name_plural': 'フィールドスタッフ',
                'db_table': 'rugby_field_staff',
            },
        ),
        migrations.CreateModel(
            name='Half',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'created_at',
                    models.DateTimeField(auto_now_add=True, verbose_name='作成日時'),
                ),
                (
                    'updated_at',
                    models.DateTimeField(auto_now=True, verbose_name='更新日時'),
                ),
                (
                    'deleted_at',
                    models.DateTimeField(blank=True, null=True, verbose_name='削除日時'),
                ),
                ('duration', models.DurationField(verbose_name='時間')),
                ('number', models.IntegerField(verbose_name='序数')),
            ],
            options={'verbose_name_plural': 'ハーフ', 'db_table': 'rugby_half'},
        ),
        migrations.CreateModel(
            name='TeamOnMatch',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'created_at',
                    models.DateTimeField(auto_now_add=True, verbose_name='作成日時'),
                ),
                (
                    'updated_at',
                    models.DateTimeField(auto_now=True, verbose_name='更新日時'),
                ),
                (
                    'deleted_at',
                    models.DateTimeField(blank=True, null=True, verbose_name='削除日時'),
                ),
                ('name', models.CharField(max_length=35, verbose_name='チーム名')),
                (
                    'team_group',
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to='member.TeamGroup',
                        verbose_name='チームグループ',
                    ),
                ),
            ],
            options={
                'verbose_name_plural': '試合参加チーム',
                'db_table': 'rugby_team_on_match',
            },
        ),
        migrations.CreateModel(
            name='PlayerOnMatch',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'created_at',
                    models.DateTimeField(auto_now_add=True, verbose_name='作成日時'),
                ),
                (
                    'updated_at',
                    models.DateTimeField(auto_now=True, verbose_name='更新日時'),
                ),
                (
                    'deleted_at',
                    models.DateTimeField(blank=True, null=True, verbose_name='削除日時'),
                ),
                ('position_number', models.PositiveIntegerField(verbose_name='背番号')),
                (
                    'member',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to='member.Member',
                        verbose_name='メンバー',
                    ),
                ),
                (
                    'team',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to='match.TeamOnMatch',
                        verbose_name='所属チーム',
                    ),
                ),
            ],
            options={
                'verbose_name_plural': '試合登録プレイヤー',
                'db_table': 'rugby_player_on_match',
                'unique_together': {('team', 'member'), ('team', 'position_number')},
            },
        ),
        migrations.CreateModel(
            name='MatchSwitchEvent',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'created_at',
                    models.DateTimeField(auto_now_add=True, verbose_name='作成日時'),
                ),
                (
                    'updated_at',
                    models.DateTimeField(auto_now=True, verbose_name='更新日時'),
                ),
                (
                    'deleted_at',
                    models.DateTimeField(blank=True, null=True, verbose_name='削除日時'),
                ),
                ('duration', models.DurationField(verbose_name='経過時間')),
                (
                    'event_type',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to='master.MatchSwitchEventType',
                        verbose_name='試合中交替/入替イベント種別',
                    ),
                ),
                (
                    'half',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to='match.Half',
                        verbose_name='ハーフ',
                    ),
                ),
                (
                    'in_member',
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name='match_in',
                        to='match.PlayerOnMatch',
                        verbose_name='出場メンバー',
                    ),
                ),
                (
                    'out_member',
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name='match_out',
                        to='match.PlayerOnMatch',
                        verbose_name='退場メンバー',
                    ),
                ),
            ],
            options={
                'verbose_name_plural': '試合中交替/入替イベント',
                'db_table': 'rugby_match_switch_event',
            },
        ),
        migrations.CreateModel(
            name='MatchScoringEvent',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'created_at',
                    models.DateTimeField(auto_now_add=True, verbose_name='作成日時'),
                ),
                (
                    'updated_at',
                    models.DateTimeField(auto_now=True, verbose_name='更新日時'),
                ),
                (
                    'deleted_at',
                    models.DateTimeField(blank=True, null=True, verbose_name='削除日時'),
                ),
                ('duration', models.DurationField(verbose_name='経過時間')),
                ('is_no_kick', models.BooleanField(verbose_name='キック蹴らず')),
                (
                    'half',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to='match.Half',
                        verbose_name='ハーフ',
                    ),
                ),
                (
                    'method',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to='master.ScoringMethod',
                        verbose_name='得点手法',
                    ),
                ),
                (
                    'player',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to='match.PlayerOnMatch',
                        verbose_name='得点メンバー',
                    ),
                ),
            ],
            options={
                'verbose_name_plural': '試合中得点イベント',
                'db_table': 'rugby_match_scoring_event',
            },
        ),
        migrations.CreateModel(
            name='MatchPatternedEvent',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'created_at',
                    models.DateTimeField(auto_now_add=True, verbose_name='作成日時'),
                ),
                (
                    'updated_at',
                    models.DateTimeField(auto_now=True, verbose_name='更新日時'),
                ),
                (
                    'deleted_at',
                    models.DateTimeField(blank=True, null=True, verbose_name='削除日時'),
                ),
                ('duration', models.DurationField(verbose_name='経過時間')),
                (
                    'event_type',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to='master.PatternType',
                        verbose_name='試合中交替/入替イベント種別',
                    ),
                ),
                (
                    'half',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to='match.Half',
                        verbose_name='ハーフ',
                    ),
                ),
            ],
            options={
                'verbose_name_plural': '通常試合イベント',
                'db_table': 'rugby_match_patterned_event',
            },
        ),
        migrations.CreateModel(
            name='MatchFoulEvent',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'created_at',
                    models.DateTimeField(auto_now_add=True, verbose_name='作成日時'),
                ),
                (
                    'updated_at',
                    models.DateTimeField(auto_now=True, verbose_name='更新日時'),
                ),
                (
                    'deleted_at',
                    models.DateTimeField(blank=True, null=True, verbose_name='削除日時'),
                ),
                ('duration', models.DurationField(verbose_name='経過時間')),
                (
                    'card_choice',
                    models.CharField(
                        choices=[
                            ('safe', 'No Card'),
                            ('yellow', 'Yellow Card'),
                            ('red', 'Red Card'),
                        ],
                        max_length=6,
                    ),
                ),
                (
                    'half',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to='match.Half',
                        verbose_name='ハーフ',
                    ),
                ),
                (
                    'method',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to='master.FoulMethod',
                        verbose_name='反則手法',
                    ),
                ),
                (
                    'out_event',
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to='match.MatchSwitchEvent',
                        verbose_name='退場イベント',
                    ),
                ),
                (
                    'penalty_try',
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to='match.MatchScoringEvent',
                        verbose_name='ペナルティトライイベント',
                    ),
                ),
                (
                    'player',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to='match.PlayerOnMatch',
                        verbose_name='反則メンバー',
                    ),
                ),
            ],
            options={
                'verbose_name_plural': '試合中反則イベント',
                'db_table': 'rugby_match_foul_event',
            },
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'created_at',
                    models.DateTimeField(auto_now_add=True, verbose_name='作成日時'),
                ),
                (
                    'updated_at',
                    models.DateTimeField(auto_now=True, verbose_name='更新日時'),
                ),
                (
                    'deleted_at',
                    models.DateTimeField(blank=True, null=True, verbose_name='削除日時'),
                ),
                ('held_datetime', models.DateTimeField()),
                (
                    'assistant_referee',
                    models.ManyToManyField(
                        related_name='match_assistant_referee',
                        to='member.Member',
                        verbose_name='アシスタントレフリー',
                    ),
                ),
                (
                    'left_team',
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name='match_left',
                        to='match.TeamOnMatch',
                        verbose_name='左チーム',
                    ),
                ),
                (
                    'match_type',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to='master.MatchType',
                        verbose_name='試合種別',
                    ),
                ),
                (
                    'referee',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name='match_referee',
                        to='member.Member',
                        verbose_name='レフリー',
                    ),
                ),
                (
                    'right_team',
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name='match_right',
                        to='match.TeamOnMatch',
                        verbose_name='右チーム',
                    ),
                ),
                (
                    'touch_judge',
                    models.ManyToManyField(
                        related_name='match_touch_judge',
                        to='member.Member',
                        verbose_name='タッチジャッジ',
                    ),
                ),
            ],
            options={'verbose_name_plural': '試合', 'db_table': 'rugby_match'},
        ),
        migrations.AddField(
            model_name='half',
            name='match',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to='match.Match',
                verbose_name='試合',
            ),
        ),
        migrations.CreateModel(
            name='StaffOnMatch',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'created_at',
                    models.DateTimeField(auto_now_add=True, verbose_name='作成日時'),
                ),
                (
                    'updated_at',
                    models.DateTimeField(auto_now=True, verbose_name='更新日時'),
                ),
                (
                    'deleted_at',
                    models.DateTimeField(blank=True, null=True, verbose_name='削除日時'),
                ),
                (
                    'field_staff',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to='match.FieldStaff',
                        verbose_name='フィールドスタッフ職',
                    ),
                ),
                (
                    'member',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to='member.Member',
                        verbose_name='メンバー',
                    ),
                ),
                (
                    'team',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to='match.TeamOnMatch',
                        verbose_name='所属チーム',
                    ),
                ),
            ],
            options={
                'verbose_name_plural': '試合参加スタッフ',
                'db_table': 'rugby_staff_on_match',
                'unique_together': {('team', 'member')},
            },
        ),
        migrations.AlterUniqueTogether(
            name='half', unique_together={('match', 'number')}
        ),
    ]
