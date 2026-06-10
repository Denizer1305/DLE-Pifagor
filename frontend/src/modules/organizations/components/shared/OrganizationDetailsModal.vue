<script setup lang="ts">
interface Props {
    isOpen: boolean;
    title?: string;
}

interface Emits {
    (event: "close"): void;
}

withDefaults(defineProps<Props>(), {
    title: "Подробная информация",
});

defineEmits<Emits>();
</script>

<template>
    <Teleport to="body">
        <Transition name="modal-fade">
            <div
                v-if="isOpen"
                class="org-details-modal"
                role="dialog"
                aria-modal="true"
                :aria-label="title"
                @click.self="$emit('close')"
            >
                <section class="org-details-modal__panel">
                    <header class="org-details-modal__header">
                        <span class="dashboard-badge">
                            <i class="fas fa-circle-info"></i>
                            {{ title }}
                        </span>

                        <button
                            class="org-details-modal__close"
                            type="button"
                            aria-label="Закрыть"
                            @click="$emit('close')"
                        >
                            <i class="fas fa-xmark"></i>
                        </button>
                    </header>

                    <div class="org-details-modal__body">
                        <slot />
                    </div>
                </section>
            </div>
        </Transition>
    </Teleport>
</template>
