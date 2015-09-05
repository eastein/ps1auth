from django.utils import timezone

from rest_framework import serializers

from member_management.models import Person, PayPal


class PayPalSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayPal
        fields = ('email',)


class PersonSerializer(serializers.HyperlinkedModelSerializer):
    paypal = PayPalSerializer()
    id = serializers.ReadOnlyField()

    class Meta:
        model = Person
        fields = ('id', 'first_name', 'last_name', 'email', 'membership_status', 'membership_start_date', 'paypal')

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.membership_status = validated_data.get('membership_status', instance.membership_status)
        instance.membership_start_date = validated_data.get('membership_start_date', instance.membership_start_date)
        paypal_email = validated_data.get('paypal', {}).get('email', None)
        if paypal_email:
            if instance.paypal:
                instance.paypal.email = validated_data.get('paypal', {}).get('email', None)
            else:
                instance.paypal = PayPal(email=paypal_email)
            instance.paypal.save()
        instance.save()
        return instance

    def create(self, validated_data):
        person = Person(first_name=validated_data.get('first_name', None),
                        last_name=validated_data.get('last_name',None),
                        email=validated_data.get('email',None,),
                        membership_status=validated_data.get('membership_status', 'discontinued'),
                        membership_start_date=validated_data.get('membership_start_date',timezone.now().date()))
        person.save()
        paypal = PayPal(person=person,email=validated_data['paypal']['email'])
        paypal.save()
        return person
