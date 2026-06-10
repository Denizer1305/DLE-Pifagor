<script setup lang="ts">
interface Props {
    label: string;
    text?: string;
    modelValue: boolean;
    disabled?: boolean;
}

interface Emits {
    (event: "update:modelValue", value: boolean): void;
}

defineProps<Props>();
const emit = defineEmits<Emits>();

function handleChange(event: Event): void {
    const input = event.target as HTMLInputElement;

    emit("update:modelValue", input.checked);
}
</script>

<template>
    <label class="settings-toggle-row">
        <span class="settings-toggle-copy">
            <strong>{{ label }}</strong>
            <span v-if="text">{{ text }}</span>
        </span>

        <input
            type="checkbox"
            :checked="modelValue"
            :disabled="disabled"
            @change="handleChange"
        />

        <span class="settings-toggle-ui"></span>
    </label>
</template>
