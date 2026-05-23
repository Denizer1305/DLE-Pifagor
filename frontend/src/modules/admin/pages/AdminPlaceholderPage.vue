<script setup lang="ts">
import { useRoute } from "vue-router";

const route = useRoute();
</script>

<template>
    <main class="dashboard-main">
        <div class="dashboard-main-inner">
            <section class="dashboard-placeholder">
                <div class="dashboard-placeholder-card">
                    <span class="dashboard-placeholder-label">
                        Раздел в разработке
                    </span>

                    <h1>
                        {{ route.meta.title || "Административный раздел" }}
                    </h1>

                    <p>
                        Эта страница будет реализована после главного кабинета администратора.
                    </p>
                </div>
            </section>
        </div>
    </main>
</template>