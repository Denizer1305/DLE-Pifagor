import { computed, onMounted, ref } from "vue";
import { useRoute } from "vue-router";

import { verifyEmail } from "@/modules/auth/api/auth.api";

export type VerifyEmailStatus = "idle" | "loading" | "success" | "error";

export function useVerifyEmailForm() {
    const route = useRoute();

    const status = ref<VerifyEmailStatus>("idle");
    const message = ref("Проверяем ссылку подтверждения. Это займёт несколько секунд.");

    const token = computed(() => {
        const value = route.query.token;

        if (typeof value === "string") {
            return value;
        }

        return "";
    });

    const isLoading = computed(() => {
        return status.value === "loading";
    });

    const isSuccess = computed(() => {
        return status.value === "success";
    });

    const isError = computed(() => {
        return status.value === "error";
    });

    async function submitVerification(): Promise<void> {
        if (status.value === "loading") {
            return;
        }

        if (!token.value) {
            status.value = "error";
            message.value = "В ссылке подтверждения нет токена. Попробуйте открыть письмо ещё раз.";

            return;
        }

        status.value = "loading";
        message.value = "Проверяем ссылку подтверждения. Это займёт несколько секунд.";

        try {
            await verifyEmail({
                token: token.value,
            });

            status.value = "success";
            message.value = "Email успешно подтверждён. Теперь можно войти в аккаунт.";
        } catch (error) {
            status.value = "error";

            if (error instanceof Error) {
                message.value = error.message;
                return;
            }

            message.value = "Не удалось подтвердить email. Возможно, ссылка устарела.";
        }
    }

    onMounted(() => {
        void submitVerification();
    });

    return {
        token,
        status,
        message,
        isLoading,
        isSuccess,
        isError,
        submitVerification,
    };
}