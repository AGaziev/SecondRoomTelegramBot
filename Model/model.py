from peewee import *

db = SqliteDatabase('db/SecondRoomDatabase')


class BaseModel(Model):
    id = PrimaryKeyField(unique=True)

    class Meta:
        database = db
        order_by = 'id'


class Category(BaseModel):
    title = CharField()

    class Meta:
        db_table = 'Category'


class Subcategory(BaseModel):
    title = CharField()
    of_category = ForeignKeyField(Category)

    class Meta:
        db_table = 'Subcategory'


class Role(BaseModel):
    name = CharField()
    can_post_in_group = BooleanField()
    access_admin_panel = BooleanField()
    access_statistics = BooleanField()
    access_catalog = BooleanField()
    can_delete_all = BooleanField()

    class Meta:
        db_table = 'Role'


class User(BaseModel):
    telegram_id = CharField(unique=True)
    first_name = CharField(null=True)
    last_name = CharField(null=True)
    username = CharField(null=True)
    role_id = ForeignKeyField(Role)

    class Meta:
        db_table = 'User'


class Cloth(BaseModel):
    brand = CharField(null=True)
    condition = CharField()
    cloth_name = CharField(null=True)
    price = CharField(null=True, default='FREE')
    size = CharField()
    subcategory = ForeignKeyField(Subcategory)
    category = ForeignKeyField(Category)
    seller = ForeignKeyField(User)
    timestamp = DateTimeField(default=[SQL('DEFAULT CURRENT_TIMESTAMP')])

    class Meta:
        db_table = 'Cloth'


class Photo(BaseModel):
    photoId = CharField()
    of_cloth = ForeignKeyField(Cloth)

    class Meta:
        db_table = 'Photo'


class NoveltyInfo(BaseModel):
    user_id = ForeignKeyField(User)
    subcategory_id = ForeignKeyField(Subcategory)
    category_id = ForeignKeyField(Subcategory, to_field='of_category')

    class Meta:
        db_table = 'NoveltyInfo'
