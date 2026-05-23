import { onMounted, ref } from "vue";

import { getProfileAchievementsPlaceholder } from "@/modules/profile/services/profile-achievements.service";

export function useProfileAchievements() {
    const items = ref<[]>([]);
    const isLoading = ref(false);
    const errorMessage = ref("");

    async function loadAchievements(): Promise<void> {
        isLoading.value = true;
        errorMessage.value = "";

        try {
            items.value = await getProfileAchievementsPlaceholder();
        } catch (error) {
            errorMessage.value = error instanceof Error
                ? error.message
                : "Не удалось загрузить достижения.";
        } finally {
            isLoading.value = false;
        }
    }

    onMounted(() => {
        void loadAchievements();
    });

    return {
        items,
        isLoading,
        errorMessage,
        loadAchievements,
    };
}