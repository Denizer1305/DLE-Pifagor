<script setup lang="ts">
interface Props {
    modelValue: boolean;
    error?: string;
}

interface Emits {
    (event: "update:modelValue", value: boolean): void;
}

withDefaults(defineProps<Props>(), {
    error: "",
});

const emit = defineEmits<Emits>();

function updateAgreement(event: Event): void {
    const input = event.target as HTMLInputElement;

    emit("update:modelValue", input.checked);
}
</script>

<template>
    <div>
        <div class="form-check">
            <input
                id="registerAgreement"
                type="checkbox"
                :checked="modelValue"
                @change="updateAgreement"
            />

            <label for="registerAgreement">
                Я принимаю условия использования платформы и согласен на обработку данных.
            </label>
        </div>

        <p
            v-if="error"
            class="form-error"
        >
            {{ error }}
        </p>
    </div>
</template>