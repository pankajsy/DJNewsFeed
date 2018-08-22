from __future__ import unicode_literals
from account.models import Basemodel
from django.contrib.gis.db import models

CATEGORY = ( ("business","business"),
             ("entertainment" ,"entertainment"),
             ("general","general"),
             ("health","health"),
             ("science","science"),
             ("sports","sports"),
             ("technology","technology"),
            ("more","more"),
            )
COUNTRY = (
("ae","ae"),
("ar","ar"),
("at","at"),
("au","au"),
("be","be"),
("bg","bg"),
("br","br"),
("ca","ca"),
("ch","ch"),
("cn","cn"),
("co","co"),
("cu","cu"),
("cz","cz"),
("de","de"),
("eg","eg"),
("fr","fr"),
("gb","gb"),
("gr","gr"),
("hk","hk"),
("hu","hu"),
("id","id"),
("ie","ie"),
("il","il"),
("in","in"),
("it","it"),
("jp","jp"),
("kr","kr"),
("lt","lt"),
("lv","lv"),
("ma","ma"),
("mx","mx"),
("my","my"),
("ng","ng"),
("nl","nl"),
("no","no"),
("nz","nz"),
("ph","ph"),
("pl","pl"),
("pt","pt"),
("ro","ro"),
("rs","rs"),
("ru","ru"),
("sa","sa"),
("se","se"),
("sg","sg"),
("si","si"),
("sk","sk"),
("th","th"),
("tr","tr"),
("tw","tw"),
("ua","ua"),
("us","us"),
("ve","ve"),
("za","za"),
)
LANGUAGE = (
("ar","ar"),
("de","de"),
("en","en"),
("es","es"),
("fr","fr"),
("he","he"),
("it","it"),
("nl","nl"),
("no","no"),
("pt","pt"),
("ru","ru"),
("se","se"),
("ud","ud"),
("zh","zh"),
("es","es"),
("fr","fr"),
("he","he"),
("it","it"),
("nl","nl"),
("no","no"),
("pt","pt"),
("ru","ru"),
("se","se"),
("ud","ud"),
("zh","zh"),
)

class Source(Basemodel):
    name = models.CharField(blank=False, null=True, max_length=100)
    uid = models.CharField(blank=False, null=True, max_length=100)
    desc = models.TextField(blank=False, null=True)
    url = models.URLField()
    category = models.CharField(choices=CATEGORY, max_length=200)
    language = models.CharField(choices=LANGUAGE, max_length=200)
    country = models.CharField(choices=COUNTRY, max_length=200)
    def __str__(self):
        return self.uid

class Article(Basemodel):
    article_source = models.ForeignKey(Source, related_name='article_source')
    published_at = models.DateTimeField(null=True, auto_now_add=False, blank=True)
    author = models.CharField(blank=True, null=True, max_length=100)
    title = models.CharField(blank=True, null=True, max_length=100)
    desc = models.TextField(blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    urltoimage = models.URLField(blank=True, null=True)
    category = models.CharField(choices=CATEGORY, max_length=200)
    country = models.CharField(choices=COUNTRY, max_length=200)


    def __str__(self):
        return self.title


