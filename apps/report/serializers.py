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

PROVINCES_FA_REVERSED = {
    "البرز": "Alborz",
    "اردبیل": "Ardabil",
    "آذربایجان شرقی": "Aazerbaijan-East",
    "بوشهر": "Bushehr",
    "چهارمحال و بختیاری": "Chahaar-Mahaal-Bakhtiaari",
    "فارس": "Fars",
    "گیلان": "Gilaan",
    "گلستان": "Golestaan",
    "همدان": "Hamadaan",
    "هرمزگان": "Hormozgaan",
    "ایلام": "Ilaam",
    "اصفهان": "Isfahaan",
    "کرمان": "Kermaan",
    "کرمانشاه": "Kermanshaah",
    "خراسان شمالی": "Khoraasaan-North",
    "خراسان رضوی": "Khoraasaan-Razavi",
    "خراسان جنوبی": "Khoraasaan-South",
    "خوزستان": "Khuzestaan",
    "کهگیلوی و بویراحمد": "Kohgiluyeh-Boyer-Ahmad",
    "کردستان": "Kurdistaan",
    "لرستان": "Lorestaan",
    "مرکزی": "Markazi",
    "مازندران": "Maazandaraan",
    "قزوین": "Qazvin",
    "قم": "Qom",
    "سمنان": "Semnaan",
    "سیستان و بلوچستان": "Sistaan-Baluchestaan",
    "تهران": "Tehran",
    "یزد": "Yazd",
    "زنجان": "Zanjaan",
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
    app_id = serializers.CharField(source='app.id')

    class Meta:
        model = Test
        fields = '__all__'

    def get_date(self, obj):
        if obj.date:
            jalali_date = jdatetime.date.fromgregorian(date=obj.date)
            return f"{jalali_date.year:04d}/{jalali_date.month:02d}/{jalali_date.day:02d}"
        return None

    def get_app_id(self, obj):
        name = obj.app.id if obj.app else ""
        return name

class AddRecordSerializer(serializers.Serializer):
    app = serializers.CharField(max_length=255)
    isp = serializers.CharField(max_length=255)
    city = serializers.CharField(max_length=255)
    status = serializers.CharField(max_length=255)

    def validate(self, attrs):
        for key, value in attrs.items():
            attrs[key] = value.strip()
        return attrs

