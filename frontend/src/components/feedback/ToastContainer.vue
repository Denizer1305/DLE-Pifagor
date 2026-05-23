<script setup lang="ts">
import { useToastStore } from "@/stores/toast.store";

interface Props {
    closeLabel: string;
}

defineProps<Props>();

const toastStore = useToastStore();

function getIconClass(type: string): string {
    if (type === "success") {
        return "fa-solid fa-circle-check";
    }

    if (type === "error") {
        return "fa-solid fa-circle-exclamation";
    }

    if (type === "warning") {
        return "fa-solid fa-triangle-exclamation";
    }

    return "fa-solid fa-circle-info";
}
</script>

<template>
    <Teleport to="body">
        <TransitionGroup
            name="toast"
            tag="div"
            class="toast-container"
        >
            <article
                v-for="toast in toastStore.items"
                :key="toast.id"
                :class="['toast-card', `toast-card--${toast.type}`]"
            >
                <div class="toast-card__icon">
                    <i :class="getIconClass(toast.type)"></i>
                </div>

                <div class="toast-card__content">
                    <strong
                        v-if="toast.title"
                        class="toast-card__title"
                    >
                        {{ toast.title }}
                    </strong>

                    <p class="toast-card__message">
                        {{ toast.message }}
                    </p>
                </div>

                <button
                    class="toast-card__close"
                    type="button"
                    :aria-label="closeLabel"
                    @click="toastStore.removeToast(toast.id)"
                >
                    <i class="fa-solid fa-xmark"></i>
                </button>
            </article>
        </TransitionGroup>
    </Teleport>
</template>
