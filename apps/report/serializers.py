from rest_framework import serializers

from apps.test.models import Isp, App,Test

import jdatetime

PROVINCES_FA = {
    "Alborz": "البرز",
    "Ardabil": "اردبیل",
    "Aazerbaijan-East": "آذربایجان شرقی",
    "Bushehr": "بوشهر",
    "Chahaar-Mahaal-Bakhtiaari": "چهارمحال و بختیاری",
    "Fars": "فارس",
    "Gilaan": "گیلان",
    "Golestaan": "گلستان",
    "Hamadaan": "همدان",
    "Hormozgaan": "هرمزگان",
    "Ilaam": "ایلام",
    "Isfahaan": "اصفهان",
    "Kermaan": "کرمان",
    "Kermanshaah": "کرمانشاه",
    "Khoraasaan-North": "خراسان شمالی",
    "Khoraasaan-Razavi": "خراسان رضوی",
    "Khoraasaan-South": "خراسان جنوبی",
    "Khuzestaan": "خوزستان",
    "Kohgiluyeh-Boyer-Ahmad": "کهگیلوی و بویراحمد",
    "Kurdistaan": "کردستان",
    "Lorestaan": "لرستان",
    "Markazi": "مرکزی",
    "Maazandaraan": "مازندران",
    "Qazvin": "قزوین",
    "Qom": "قم",
    "Semnaan": "سمنان",
    "Sistaan-Baluchestaan": "سیستان و بلوچستان",
    "Tehran": "تهران",
    "Yazd": "یزد",
    "Zanjaan": "زنجان",

}


class GetAllIspAPISerializer(serializers.ModelSerializer):
    class Meta:
        model = Isp
        fields = ['id', 'name', 'url', 'org', 'as_number', 'asname']


class GetAllAppAPISerializer(serializers.ModelSerializer):
    class Meta:
        model = App
        fields = ['id', 'name']


class EndTestSerializer(serializers.ModelSerializer):
    date = serializers.SerializerMethodField()
    app = serializers.CharField(source='app.name')
    isp = serializers.CharField(source='isp.name')
    name2 = serializers.SerializerMethodField()

    class Meta:
        model = Test
        fields = '__all__'

    def get_date(self, obj):
        if obj.date:
            jalali_date = jdatetime.date.fromgregorian(date=obj.date)
            return f"{jalali_date.year:04d}/{jalali_date.month:02d}/{jalali_date.day:02d}"
        return None

    def get_name2(self, obj):
        name = obj.app.name if obj.app else ""
        return name.replace(" ", "").lower()

