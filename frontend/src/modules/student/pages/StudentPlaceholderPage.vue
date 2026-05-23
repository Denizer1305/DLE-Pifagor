<script setup lang="ts">
import { useRoute } from "vue-router";

const route = useRoute();
</script>

<template>
    <main class="dashboard-placeholder-page">
        <section class="dashboard-card">
            <div class="dashboard-card-inner">
                <div class="dashboard-card-topline">
                    <i class="fas fa-user-graduate"></i>
                    Личный кабинет студента
                </div>

                <h1 class="dashboard-section-title">
                    Раздел в подготовке
                </h1>

                <p class="dashboard-section-text">
                    {{ route.meta.title || "Этот раздел личного кабинета будет подключён позже." }}
                </p>
            </div>
        </section>
    </main>
</template>
