<script setup lang="ts">
import { useI18n } from "@/composables/useI18n";

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
const { tr } = useI18n();

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
                {{ tr("Я принимаю условия использования платформы и согласен на обработку данных.") }}
            </label>
        </div>

        <p
            v-if="error"
            class="form-error"
        >
            {{ tr(error) }}
        </p>
    </div>
</template>
