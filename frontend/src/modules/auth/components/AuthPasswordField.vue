<script setup lang="ts">
import { usePasswordToggle } from "@/modules/auth/composables/usePasswordToggle";

interface Props {
    id: string;
    modelValue: string;
    label: string;
    placeholder?: string;
    autocomplete?: string;
    required?: boolean;
    error?: string;
}

interface Emits {
    (event: "update:modelValue", value: string): void;
}

const props = withDefaults(defineProps<Props>(), {
    placeholder: "",
    autocomplete: "current-password",
    required: false,
    error: "",
});

const emit = defineEmits<Emits>();

const {
    inputType,
    iconClass,
    ariaLabel,
    togglePasswordVisibility,
} = usePasswordToggle();

function updateValue(event: Event): void {
    const input = event.target as HTMLInputElement;

    emit("update:modelValue", input.value);
}
</script>

<template>
    <div class="form-group">
        <label
            class="form-label"
            :for="id"
        >
            {{ label }}
        </label>

        <div class="password-field">
            <input
                :id="id"
                class="form-input"
                :class="{ 'is-invalid': props.error }"
                :type="inputType"
                :value="modelValue"
                :placeholder="placeholder"
                :autocomplete="autocomplete"
                :required="required"
                @input="updateValue"
            />

            <button
                class="password-toggle"
                type="button"
                :aria-label="ariaLabel"
                @click="togglePasswordVisibility"
            >
                <i :class="iconClass"></i>
            </button>
        </div>

        <p
            v-if="props.error"
            class="form-error"
        >
            {{ props.error }}
        </p>
    </div>
</template>