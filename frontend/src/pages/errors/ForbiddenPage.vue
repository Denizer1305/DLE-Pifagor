<script setup lang="ts">
import { RouterLink } from "vue-router";
</script>

<template>
    <section class="error-page">
        <div class="error-page__card">
            <p class="error-page__code">403</p>

            <h1 class="error-page__title">
                Доступ ограничен
            </h1>

            <p class="error-page__text">
                У вашей роли нет доступа к этому разделу платформы.
            </p>

            <RouterLink
                class="error-page__button"
                :to="{ name: 'home' }"
            >
                Вернуться на главную
            </RouterLink>
        </div>
    </section>
</template>
