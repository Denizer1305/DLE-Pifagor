import { computed, ref } from "vue";
import type { PublicTeacher } from "@/modules/public/types/public-teachers.types";

export function useTeacherModal() {
    const selectedTeacher = ref<PublicTeacher | null>(null);

    const isTeacherModalOpen = computed(() => Boolean(selectedTeacher.value));

    function openTeacherModal(teacher: PublicTeacher) {
        selectedTeacher.value = teacher;
    }

    function closeTeacherModal() {
        selectedTeacher.value = null;
    }

    return {
        selectedTeacher,
        isTeacherModalOpen,
        openTeacherModal,
        closeTeacherModal,
    };
}
