<script setup lang="ts">
import { computed } from "vue";
import { useRoute, useRouter } from "vue-router";

const route = useRoute();
const router = useRouter();

const title = computed(() => {
    return route.meta.title?.toString() || "Раздел преподавателя";
});

function goBack(): void {
    router.back();
}
</script>

<template>
    <main class="teacher-dashboard-page">
        <section class="dashboard-card teacher-placeholder-page">
            <div class="dashboard-card-inner">
                <div class="dashboard-card-topline">
                    <i class="fas fa-screwdriver-wrench"></i>
                    Раздел в разработке
                </div>

                <h1 class="dashboard-section-title">
                    {{ title }}
                </h1>

                <p class="dashboard-section-text">
                    Эта страница уже добавлена в маршрутизацию, чтобы личный кабинет преподавателя
                    не падал при переходах. Позже здесь будет полноценный интерфейс раздела.
                </p>

                <div class="dashboard-course-actions">
                    <RouterLink
                        class="dashboard-course-btn primary"
                        :to="{ name: 'teacher-dashboard' }"
                    >
                        Вернуться в кабинет
                    </RouterLink>

                    <button
                        type="button"
                        class="dashboard-course-btn"
                        @click="goBack"
                    >
                        Назад
                    </button>
                </div>
            </div>
        </section>
    </main>
</template>