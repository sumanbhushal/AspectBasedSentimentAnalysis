# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Bigrams(models.Model):
    review_id = models.IntegerField(blank=True, null=True)
    sentence_id = models.IntegerField(blank=True, null=True)
    bigrams = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bigrams'


class CandidateAspect(models.Model):
    review_id = models.IntegerField(blank=True, null=True)
    sentence_id = models.IntegerField(blank=True, null=True)
    candidate_aspect = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'candidate_aspect'


class CandidateAspectsFinal(models.Model):
    aspect = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'candidate_aspects_final'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class FinalAspects(models.Model):
    final_aspects = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'final_aspects'


class FrequentItemsets(models.Model):
    frequent_itemsets = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'frequent_itemsets'


class FrequentItemsetsK(models.Model):
    frequent_itemsets = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'frequent_itemsets_k'


class NounsChunksPerSentence(models.Model):
    noun_chunk_id = models.AutoField(primary_key=True)
    review_id = models.IntegerField(blank=True, null=True)
    sentence_id = models.IntegerField(blank=True, null=True)
    nouns = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'nouns_chunks_per_sentence'


class NounsListPerSentence(models.Model):
    noun_list_id = models.AutoField(primary_key=True)
    review_id = models.IntegerField(blank=True, null=True)
    sentence_id = models.IntegerField(blank=True, null=True)
    nouns = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'nouns_list_per_sentence'


class Pentagrams(models.Model):
    review_id = models.IntegerField(blank=True, null=True)
    sentence_id = models.IntegerField(blank=True, null=True)
    pentagrams = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pentagrams'


class PosTaggedSentences(models.Model):
    sentence_id = models.IntegerField(primary_key=True)
    review_id = models.IntegerField(blank=True, null=True)
    pos_tagged_sentences = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pos_tagged_sentences'


class ProductAspects(models.Model):
    aspect = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'product_aspects'


class Pruning(models.Model):
    candidate_features = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pruning'


class Quadgrams(models.Model):
    review_id = models.IntegerField(blank=True, null=True)
    sentence_id = models.IntegerField(blank=True, null=True)
    quadgrams = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'quadgrams'


class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    review = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'review'


class Sentences(models.Model):
    sentences_id = models.AutoField(primary_key=True)
    review_id = models.IntegerField(blank=True, null=True)
    sentence = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sentences'

    def __str__(self):
        return u'%s' % (self.sentence)

class SentimentAnalysis(models.Model):
    id = models.IntegerField(blank=False, null=False, primary_key=True)
    product_aspect = models.CharField(max_length=75, blank=True, null=True)
    pos_score = models.IntegerField(blank=True, null=True)
    neg_score = models.IntegerField(blank=True, null=True)
    neu_score = models.IntegerField(blank=True, null=True)
    pos_sent_ids = models.CharField(max_length=255, blank=True, null=True)
    neg_sent_ids = models.CharField(max_length=255, blank=True, null=True)
    neu_sent_ids = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sentiment_analysis'

    def __str__(self):
        return u'%s %s %s %s %s %s %s' % (self.id, self.product_aspect, self.pos_score, self.neg_score, self.neu_score,
                           self.pos_sent_ids, self.neg_sent_ids, self.neu_sent_ids)

class Trigrams(models.Model):
    review_id = models.IntegerField(blank=True, null=True)
    sentence_id = models.IntegerField(blank=True, null=True)
    trigrams = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'trigrams'


class Unigram(models.Model):
    review_id = models.IntegerField(blank=True, null=True)
    sentence_id = models.IntegerField(blank=True, null=True)
    unigram = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'unigram'
