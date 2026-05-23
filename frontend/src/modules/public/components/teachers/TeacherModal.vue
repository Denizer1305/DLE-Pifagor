<script setup lang="ts">
import { computed, onBeforeUnmount, watch } from "vue";

import { useI18n } from "@/composables/useI18n";
import type { PublicTeacher } from "@/modules/public/types/public-teachers.types";

interface Props {
    teacher: PublicTeacher | null;
    isOpen: boolean;
}

interface Emits {
    (event: "close"): void;
}

const props = defineProps<Props>();
const emit = defineEmits<Emits>();
const { t } = useI18n();

const modalTitleId = computed(() => {
    if (!props.teacher) {
        return "teacher-modal-title";
    }

    return `teacher-${props.teacher.id}-title`;
});

function closeModal(): void {
    emit("close");
}

function handleKeydown(event: KeyboardEvent): void {
    if (event.key === "Escape") {
        closeModal();
    }
}

watch(
    () => props.isOpen,
    (isOpen) => {
        document.body.classList.toggle("is-modal-open", isOpen);

        if (isOpen) {
            window.addEventListener("keydown", handleKeydown);
            return;
        }

        window.removeEventListener("keydown", handleKeydown);
    },
    {
        immediate: true,
    },
);

onBeforeUnmount(() => {
    document.body.classList.remove("is-modal-open");
    window.removeEventListener("keydown", handleKeydown);
});
</script>

<template>
    <Teleport to="body">
        <div
            class="modal-overlay"
            :class="{ active: isOpen && teacher }"
            :aria-hidden="!isOpen"
            @click.self="closeModal"
        >
            <div
                v-if="teacher"
                class="modal-window teacher-modal"
                role="dialog"
                aria-modal="true"
                :aria-labelledby="modalTitleId"
                @click.stop
            >
                <button
                    class="modal-close"
                    type="button"
                    :aria-label="t('common.closeWindow')"
                    @click="closeModal"
                >
                    <i class="fas fa-times"></i>
                </button>

                <div class="teacher-modal-content">
                    <div class="teacher-modal-media">
                        <img
                            :src="teacher.image.src"
                            :alt="teacher.image.alt"
                        />
                    </div>

                    <div class="teacher-modal-panel">
                        <div class="teacher-modal-topline">
                            {{ teacher.role }}
                        </div>

                        <h3
                            :id="modalTitleId"
                            class="teacher-modal-name"
                        >
                            {{ teacher.name }}
                        </h3>

                        <div class="teacher-modal-subject">
                            {{ teacher.direction }}
                        </div>

                        <p class="teacher-modal-description">
                            {{ teacher.description }}
                        </p>

                        <div
                            v-if="teacher.tags.length"
                            class="teacher-modal-tags"
                        >
                            <span
                                v-for="tag in teacher.tags"
                                :key="tag"
                                class="teacher-modal-tag"
                            >
                                {{ tag }}
                            </span>
                        </div>

                        <div
                            v-if="teacher.awards.length"
                            class="teacher-modal-section"
                        >
                            <div class="teacher-modal-section-title">
                                {{ t("teachers.awards") }}
                            </div>

                            <ul class="teacher-modal-awards">
                                <li
                                    v-for="award in teacher.awards"
                                    :key="award"
                                >
                                    <i class="fas fa-award"></i>
                                    <span>{{ award }}</span>
                                </li>
                            </ul>
                        </div>

                        <div
                            v-if="teacher.department"
                            class="teacher-modal-section"
                        >
                            <div class="teacher-modal-section-title">
                                {{ t("teachers.department") }}
                            </div>

                            <p class="teacher-modal-description">
                                {{ teacher.department.name }}
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </Teleport>
</template>
