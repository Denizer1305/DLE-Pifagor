<script setup lang="ts">
interface Props {
    title?: string;
    text?: string;
    hint?: string;
    isCollapsed?: boolean;
    applyLabel?: string;
    resetLabel?: string;
}

interface Emits {
    (event: "apply"): void;
    (event: "reset"): void;
}

withDefaults(defineProps<Props>(), {
    title: "",
    text: "",
    hint: "",
    isCollapsed: false,
    applyLabel: "",
    resetLabel: "",
});

defineEmits<Emits>();
</script>

<template>
    <section
        class="org-filters"
        :class="{ 'is-collapsed': isCollapsed }"
    >
        <header
            v-if="title || text || $slots.header"
            class="org-filters__header"
        >
            <slot name="header">
                <div>
                    <h2
                        v-if="title"
                        class="org-filters__title"
                    >
                        {{ title }}
                    </h2>

                    <p
                        v-if="text"
                        class="org-filters__text"
                    >
                        {{ text }}
                    </p>
                </div>
            </slot>
        </header>

        <div class="org-filters__grid">
            <slot />
        </div>

        <slot name="chips" />

        <footer
            v-if="hint || applyLabel || resetLabel || $slots.footer"
            class="org-filters__footer"
        >
            <slot name="footer">
                <p
                    v-if="hint"
                    class="org-filters__hint"
                >
                    {{ hint }}
                </p>

                <div class="org-filters__actions">
                    <button
                        v-if="resetLabel"
                        class="org-filters__button"
                        type="button"
                        @click="$emit('reset')"
                    >
                        {{ resetLabel }}
                    </button>

                    <button
                        v-if="applyLabel"
                        class="org-filters__button org-filters__button--primary"
                        type="button"
                        @click="$emit('apply')"
                    >
                        {{ applyLabel }}
                    </button>
                </div>
            </slot>
        </footer>
    </section>
</template>
