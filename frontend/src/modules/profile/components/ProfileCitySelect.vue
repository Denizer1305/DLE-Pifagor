<script setup lang="ts">
import { ref } from "vue";

import type { ProfileCitySuggestion } from "@/modules/profile/types/profile-edit.types";

interface Props {
    modelValue: string;
    suggestions: ProfileCitySuggestion[];
    isLoading?: boolean;
}

interface Emits {
    (event: "update:modelValue", value: string): void;
    (event: "search", value: string): void;
    (event: "select", suggestion: ProfileCitySuggestion): void;
}

defineProps<Props>();
const emit = defineEmits<Emits>();
const isOpen = ref(false);
const hasRequested = ref(false);

function handleInput(event: Event): void {
    const value = (event.target as HTMLInputElement).value;

    isOpen.value = true;
    hasRequested.value = value.trim().length >= 2;
    emit("update:modelValue", value);
    emit("search", value);
}

function selectSuggestion(suggestion: ProfileCitySuggestion): void {
    isOpen.value = false;
    hasRequested.value = false;
    emit("select", suggestion);
}

function closeAfterFocus(): void {
    window.setTimeout(() => {
        isOpen.value = false;
    }, 120);
}
</script>

<template>
    <div
        class="profile-city-select"
        :class="{ 'is-open': isOpen }"
    >
        <div class="profile-city-select__input-wrap">
            <i class="fas fa-location-dot"></i>
            <input
                id="profile-city"
                :value="modelValue"
                type="text"
                role="combobox"
                autocomplete="off"
                placeholder="Начните вводить город"
                :aria-expanded="isOpen"
                aria-controls="profile-city-options"
                @focus="isOpen = true"
                @blur="closeAfterFocus"
                @input="handleInput"
            />
            <i
                v-if="isLoading"
                class="fas fa-spinner fa-spin profile-city-select__spinner"
            ></i>
        </div>

        <div
            v-if="isOpen && hasRequested"
            id="profile-city-options"
            class="profile-city-select__options"
            role="listbox"
        >
            <button
                v-for="suggestion in suggestions"
                :key="suggestion.unrestrictedValue"
                class="profile-city-select__option"
                type="button"
                role="option"
                @mousedown.prevent
                @click="selectSuggestion(suggestion)"
            >
                <i class="fas fa-location-dot"></i>
                <span>{{ suggestion.value }}</span>
            </button>

            <span
                v-if="isLoading && !suggestions.length"
                class="profile-city-select__state"
            >
                Ищем город...
            </span>

            <span
                v-else-if="!suggestions.length"
                class="profile-city-select__state"
            >
                Подходящий город не найден.
            </span>
        </div>
    </div>
</template>
