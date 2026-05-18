<script setup lang="ts">
import { RouterLink } from "vue-router";
</script>

<template>
    <section class="error-page">
        <div class="error-page__card">
            <p class="error-page__code">404</p>

            <h1 class="error-page__title">
                Страница не найдена
            </h1>

            <p class="error-page__text">
                Возможно, страница была перемещена или ссылка указана неверно.
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
