<script setup lang="ts">
import type {
    PasswordFormErrors,
    PasswordFormState,
    SettingsPasswordFormContent,
} from "@/modules/settings/types/settings.types";

interface Props {
    form: PasswordFormState;
    errors: PasswordFormErrors;
    content: SettingsPasswordFormContent;
    isSubmitting: boolean;
}

interface Emits {
    (event: "submit"): void;
    (event: "update-field", field: keyof PasswordFormState, value: string): void;
}

defineProps<Props>();
const emit = defineEmits<Emits>();

function updateField(field: keyof PasswordFormState, event: Event): void {
    const input = event.target as HTMLInputElement;

    emit("update-field", field, input.value);
}
</script>

<template>
    <form
        class="security-password-form"
        @submit.prevent="emit('submit')"
    >
        <div class="settings-form-grid">
            <label
                v-for="field in content.fields"
                :key="field.key"
                class="settings-input-row"
            >
                <span>
                    <strong>{{ field.label }}</strong>
                    <small>{{ field.text }}</small>
                </span>

                <input
                    :value="form[field.key]"
                    type="password"
                    :autocomplete="field.autocomplete"
                    @input="updateField(field.key, $event)"
                />

                <em v-if="errors[field.key]">
                    {{ errors[field.key] }}
                </em>
            </label>
        </div>

        <div
            v-if="errors.common"
            class="settings-error-card"
        >
            <i :class="content.errorIcon"></i>
            <span>{{ errors.common }}</span>
        </div>

        <div class="settings-actions-row">
            <button
                type="submit"
                class="settings-primary-btn"
                :disabled="isSubmitting"
            >
                <i :class="content.submitIcon"></i>
                {{ isSubmitting ? content.submittingLabel : content.submitLabel }}
            </button>
        </div>
    </form>
</template>
