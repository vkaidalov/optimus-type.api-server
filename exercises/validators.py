from rest_framework import serializers


def unique_elements_sorted_in_asc(value):
    if not all(
        value[i] < value[i + 1] for i in range(len(value) - 1)
    ):
        raise serializers.ValidationError(
            "All the elements must be unique and sorted in ascending order."
        )
