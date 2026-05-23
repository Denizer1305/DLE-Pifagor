<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref, useId } from "vue";

interface BaseSelectOption {
    value: string;
    label: string;
    disabled?: boolean;
}

interface Props {
    modelValue: string;
    options: readonly BaseSelectOption[];
    id?: string;
    placeholder?: string;
    ariaLabel?: string;
    disabled?: boolean;
    mode?: "overlay" | "inline";
    emptyText?: string;
}

interface Emits {
    (event: "update:modelValue", value: string): void;
    (event: "change", value: string): void;
}

const props = withDefaults(defineProps<Props>(), {
    placeholder: "Выберите значение",
    ariaLabel: "Открыть список",
    disabled: false,
    mode: "overlay",
    emptyText: "Нет доступных вариантов",
});
const emit = defineEmits<Emits>();
const rootRef = ref<HTMLElement | null>(null);
const isOpen = ref(false);
const focusedOptionIndex = ref(-1);
const generatedId = useId();

const controlId = computed(() => props.id || generatedId);
const listboxId = computed(() => `${controlId.value}-options`);
const selectedOption = computed(() => {
    return props.options.find((option) => option.value === props.modelValue);
});
const availableOptionIndexes = computed(() => {
    return props.options.reduce<number[]>((indexes, option, index) => {
        if (!option.disabled) {
            indexes.push(index);
        }

        return indexes;
    }, []);
});

function toggle(): void {
    if (props.disabled) {
        return;
    }

    isOpen.value = !isOpen.value;

    if (isOpen.value) {
        focusSelectedOrFirst();
    }
}

function close(): void {
    isOpen.value = false;
    focusedOptionIndex.value = -1;
}

function selectOption(option: BaseSelectOption): void {
    if (option.disabled) {
        return;
    }

    emit("update:modelValue", option.value);
    emit("change", option.value);
    close();
}

function focusSelectedOrFirst(): void {
    const selectedIndex = props.options.findIndex((option) => {
        return option.value === props.modelValue && !option.disabled;
    });

    focusedOptionIndex.value = selectedIndex >= 0
        ? selectedIndex
        : (availableOptionIndexes.value[0] ?? -1);
}

function moveFocus(direction: 1 | -1): void {
    if (!isOpen.value) {
        isOpen.value = true;
        focusSelectedOrFirst();
        return;
    }

    const indexes = availableOptionIndexes.value;
    const position = indexes.indexOf(focusedOptionIndex.value);
    const nextPosition = position < 0
        ? 0
        : (position + direction + indexes.length) % indexes.length;

    focusedOptionIndex.value = indexes[nextPosition] ?? -1;
}

function handleKeydown(event: KeyboardEvent): void {
    if (event.key === "ArrowDown") {
        event.preventDefault();
        moveFocus(1);
    }

    if (event.key === "ArrowUp") {
        event.preventDefault();
        moveFocus(-1);
    }

    if (event.key === "Enter" || event.key === " ") {
        event.preventDefault();

        if (!isOpen.value) {
            toggle();
            return;
        }

        const option = props.options[focusedOptionIndex.value];

        if (option) {
            selectOption(option);
        }
    }

    if (event.key === "Escape") {
        close();
    }
}

function handleDocumentClick(event: MouseEvent): void {
    if (!rootRef.value?.contains(event.target as Node)) {
        close();
    }
}

onMounted(() => {
    document.addEventListener("mousedown", handleDocumentClick);
});

onBeforeUnmount(() => {
    document.removeEventListener("mousedown", handleDocumentClick);
});
</script>

<template>
    <div
        ref="rootRef"
        class="custom-select"
        :class="[
            `custom-select--${mode}`,
            {
                'is-open': isOpen,
                'is-disabled': disabled,
                'is-empty': !options.length,
            },
        ]"
    >
        <button
            :id="controlId"
            class="custom-select-trigger"
            :class="{ 'is-placeholder': !selectedOption }"
            type="button"
            role="combobox"
            :disabled="disabled"
            :aria-label="ariaLabel"
            :aria-expanded="isOpen"
            :aria-controls="listboxId"
            aria-haspopup="listbox"
            @click="toggle"
            @keydown="handleKeydown"
        >
            <span class="custom-select-trigger-text">
                {{ selectedOption?.label || placeholder }}
            </span>
            <i class="fas fa-chevron-down custom-select-chevron"></i>
        </button>

        <div
            :id="listboxId"
            class="custom-select-dropdown"
            role="listbox"
        >
            <button
                v-for="(option, index) in options"
                :key="option.value"
                class="custom-select-option"
                :class="{
                    'is-selected': modelValue === option.value || focusedOptionIndex === index,
                    'is-disabled': option.disabled,
                }"
                type="button"
                role="option"
                :disabled="option.disabled"
                :aria-selected="modelValue === option.value"
                @click="selectOption(option)"
            >
                {{ option.label }}
            </button>

            <span
                v-if="!options.length"
                class="custom-select-empty"
            >
                {{ emptyText }}
            </span>
        </div>
    </div>
</template>
