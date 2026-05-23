<script setup lang="ts">
import { computed, reactive, watch } from "vue";

import BaseSelect from "@/components/base/BaseSelect.vue";
import type {
    DashboardCalendarEventType,
    DashboardCreateItemKind,
    DashboardCreateItemModalContent,
} from "@/components/dashboard/types/dashboard.types";

interface Props {
    isOpen: boolean;
    kind: DashboardCreateItemKind;
    content: DashboardCreateItemModalContent;
}

interface DashboardCreateItemPayload {
    kind: DashboardCreateItemKind;
    title: string;
    text: string;
    date: string;
    eventType: DashboardCalendarEventType;
}

const props = defineProps<Props>();

const emit = defineEmits<{
    (event: "close"): void;
    (event: "submit", payload: DashboardCreateItemPayload): void;
}>();

const form = reactive({
    title: "",
    text: "",
    date: "",
    eventType: "lesson" as DashboardCalendarEventType,
});

const modalCopy = computed(() => props.content[props.kind]);

watch(
    () => props.isOpen,
    (isOpen) => {
        if (!isOpen) {
            resetForm();
        }

        if (isOpen && !form.date) {
            form.date = getTodayDateKey();
        }
    },
);

function resetForm(): void {
    form.title = "";
    form.text = "";
    form.date = "";
    form.eventType = "lesson";
}

function getTodayDateKey(): string {
    const today = new Date();

    return [
        today.getFullYear(),
        String(today.getMonth() + 1).padStart(2, "0"),
        String(today.getDate()).padStart(2, "0"),
    ].join("-");
}

function submitForm(): void {
    const title = form.title.trim();
    const text = form.text.trim();

    if (!title) {
        return;
    }

    emit("submit", {
        kind: props.kind,
        title,
        text,
        date: form.date || getTodayDateKey(),
        eventType: form.eventType,
    });

    resetForm();
    emit("close");
}

function selectEventType(value: string): void {
    if (
        value === "lesson" ||
        value === "checking" ||
        value === "deadline" ||
        value === "system" ||
        value === "neutral"
    ) {
        form.eventType = value;
    }
}
</script>

<template>
    <Teleport to="body">
        <div
            v-if="isOpen"
            class="base-modal dashboard-create-modal is-open"
            role="dialog"
            aria-modal="true"
            :aria-labelledby="`dashboard-create-${kind}-title`"
        >
            <button
                type="button"
                class="base-modal__overlay"
                :aria-label="content.closeOverlayLabel"
                @click="emit('close')"
            ></button>

            <form
                class="base-modal__dialog dashboard-create-modal__dialog"
                @submit.prevent="submitForm"
            >
                <header class="base-modal__header">
                    <div>
                        <h2
                            :id="`dashboard-create-${kind}-title`"
                            class="base-modal__title"
                        >
                            {{ modalCopy.title }}
                        </h2>

                        <p class="base-modal__description">
                            {{ modalCopy.description }}
                        </p>
                    </div>

                    <button
                        type="button"
                        class="base-modal__close"
                        :aria-label="content.closeButtonLabel"
                        @click="emit('close')"
                    >
                        <i class="fas fa-xmark"></i>
                    </button>
                </header>

                <div class="base-modal__body dashboard-create-modal__body">
                    <label class="dashboard-create-field">
                        <span>{{ modalCopy.titleLabel }}</span>

                        <input
                            v-model="form.title"
                            type="text"
                            required
                            autocomplete="off"
                        />
                    </label>

                    <label class="dashboard-create-field">
                        <span>{{ modalCopy.dateLabel }}</span>

                        <input
                            v-model="form.date"
                            type="date"
                        />
                    </label>

                    <div
                        v-if="kind === 'calendar'"
                        class="dashboard-create-field"
                    >
                        <span>{{ modalCopy.eventTypeLabel }}</span>

                        <BaseSelect
                            id="dashboard-event-type"
                            :model-value="form.eventType"
                            :options="content.calendarEventThemeOptions"
                            :aria-label="modalCopy.eventTypeLabel"
                            @update:model-value="selectEventType"
                        />
                    </div>

                    <label class="dashboard-create-field is-wide">
                        <span>{{ modalCopy.textLabel }}</span>

                        <textarea
                            v-model="form.text"
                            rows="5"
                        ></textarea>
                    </label>
                </div>

                <footer class="base-modal__footer">
                    <button
                        type="button"
                        class="dashboard-create-modal__secondary"
                        @click="emit('close')"
                    >
                        {{ content.cancelLabel }}
                    </button>

                    <button
                        type="submit"
                        class="dashboard-create-modal__primary"
                    >
                        <i class="fas fa-plus"></i>
                        {{ modalCopy.submitLabel }}
                    </button>
                </footer>
            </form>
        </div>
    </Teleport>
</template>
