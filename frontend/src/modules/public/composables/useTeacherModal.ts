import { computed, ref } from "vue";
import type { PublicTeacher } from "@/modules/public/types/public-teachers.types";

export function useTeacherModal() {
    const selectedTeacher = ref<PublicTeacher | null>(null);

    const isTeacherModalOpen = computed(() => {
        return Boolean(selectedTeacher.value);
    });

    function openTeacher(teacher: PublicTeacher): void {
        selectedTeacher.value = teacher;
    }

    function closeTeacher(): void {
        selectedTeacher.value = null;
    }

    return {
        selectedTeacher,
        isTeacherModalOpen,
        openTeacher,
        closeTeacher,
    };
}
