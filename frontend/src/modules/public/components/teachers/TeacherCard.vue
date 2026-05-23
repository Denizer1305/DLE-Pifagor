<script setup lang="ts">
import type { PublicTeacher } from "@/modules/public/types/public-teachers.types";

interface Props {
    teacher: PublicTeacher;
}

interface Emits {
    (event: "open", teacher: PublicTeacher): void;
}

defineProps<Props>();
const emit = defineEmits<Emits>();
</script>

<template>
    <button
        class="teacher-card fade-in visible"
        type="button"
        @click="emit('open', teacher)"
    >
        <div class="teacher-card-media">
            <img
                :src="teacher.image.src"
                :alt="teacher.image.alt"
                loading="lazy"
            />
        </div>

        <div class="teacher-card-body">
            <div class="teacher-card-role">
                {{ teacher.role }}
            </div>

            <h3 class="teacher-card-name">
                {{ teacher.name }}
            </h3>

            <div class="teacher-card-subject">
                {{ teacher.subject }}
            </div>

            <div
                v-if="teacher.tags.length"
                class="teacher-card-tags"
            >
                <span
                    v-for="tag in teacher.tags.slice(0, 3)"
                    :key="tag"
                    class="teacher-card-tag"
                >
                    {{ tag }}
                </span>
            </div>
        </div>
    </button>
</template>
