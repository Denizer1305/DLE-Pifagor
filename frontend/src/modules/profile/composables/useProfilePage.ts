import { onMounted, ref } from "vue";

import { getProfilePage } from "@/modules/profile/services/profile.service";
import type {
    CurrentProfileDto,
    ProfilePageModel,
} from "@/modules/profile/types/profile.types";

export function useProfilePage() {
    const source = ref<CurrentProfileDto | null>(null);
    const pageModel = ref<ProfilePageModel | null>(null);

    const isLoading = ref(false);
    const errorMessage = ref("");

    async function loadProfile(): Promise<void> {
        isLoading.value = true;
        errorMessage.value = "";

        try {
            const result = await getProfilePage();

            source.value = result.source;
            pageModel.value = result.pageModel;
        } catch (error) {
            errorMessage.value = getProfileErrorMessage(error);
        } finally {
            isLoading.value = false;
        }
    }

    onMounted(() => {
        void loadProfile();
    });

    return {
        source,
        pageModel,
        isLoading,
        errorMessage,
        loadProfile,
    };
}

function getProfileErrorMessage(error: unknown): string {
    if (error instanceof Error && error.message) {
        return error.message;
    }

    return "Не удалось загрузить профиль пользователя.";
}
