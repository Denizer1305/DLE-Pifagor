<script setup lang="ts">
import { RouterLink } from "vue-router";

import { useI18n } from "@/composables/useI18n";

const { tr } = useI18n();
</script>

<template>
    <section class="error-page">
        <div class="error-page__card">
            <p class="error-page__code">403</p>

            <h1 class="error-page__title">
                {{ tr("Доступ ограничен") }}
            </h1>

            <p class="error-page__text">
                {{ tr("У вашей роли нет доступа к этому разделу платформы.") }}
            </p>

            <RouterLink
                class="error-page__button"
                :to="{ name: 'home' }"
            >
                {{ tr("Вернуться на главную") }}
            </RouterLink>
        </div>
    </section>
</template>
