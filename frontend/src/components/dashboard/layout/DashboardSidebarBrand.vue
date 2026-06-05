<script setup lang="ts">
import { useThemedLogo } from "@/composables/useThemedLogo";
import type { DashboardBrand } from "@/components/dashboard/types/dashboard.types";

interface Props {
    brand: DashboardBrand;
}

defineProps<Props>();
const { getThemedLogoSrc } = useThemedLogo();
</script>

<template>
    <div class="sidebar-brand">
        <img
            :src="getThemedLogoSrc(brand.logo)"
            :alt="brand.title"
        />

        <div class="sidebar-brand-text">
            <strong>{{ brand.title }}</strong>
            <span>{{ brand.subtitle }}</span>
        </div>
    </div>
</template>
