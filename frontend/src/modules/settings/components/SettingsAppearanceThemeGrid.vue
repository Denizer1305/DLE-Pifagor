<script setup lang="ts">
import type {
    AppearanceThemeModel,
    SettingsTheme,
} from "@/modules/settings/types/settings.types";

interface Props {
    themes: AppearanceThemeModel[];
    activeTheme: SettingsTheme;
    disabled?: boolean;
}

interface Emits {
    (event: "select", value: SettingsTheme): void;
}

defineProps<Props>();
const emit = defineEmits<Emits>();
</script>

<template>
    <div class="appearance-theme-grid">
        <button
            v-for="theme in themes"
            :key="theme.key"
            type="button"
            class="appearance-theme-card"
            :class="[
                theme.previewClass,
                { 'is-active': theme.key === activeTheme },
            ]"
            :disabled="disabled"
            @click="emit('select', theme.key)"
        >
            <span class="appearance-theme-preview">
                <span
                    v-for="token in theme.tokens"
                    :key="token"
                    class="appearance-theme-token"
                    :style="{ backgroundColor: token }"
                ></span>
            </span>

            <span class="appearance-theme-copy">
                <strong>{{ theme.title }}</strong>
                <span>{{ theme.text }}</span>
            </span>

            <i
                v-if="theme.key === activeTheme"
                class="fas fa-check appearance-theme-check"
            ></i>
        </button>
    </div>
</template>