<script setup lang="ts">
import type { ProfileIdentityCardModel } from "@/modules/profile/types/profile.types";

interface Props {
    card: ProfileIdentityCardModel;
}

defineProps<Props>();
</script>

<template>
    <section class="profile-identity-strip fade-in visible">
        <div class="profile-identity-card">
            <div class="profile-identity-main">
                <div class="profile-identity-topline">
                    <i class="fas fa-id-badge"></i>
                    Персональная сводка
                </div>

                <h2 class="profile-identity-title">
                    {{ card.title }}
                </h2>

                <p class="profile-identity-text">
                    {{ card.text }}
                </p>
            </div>

            <div class="profile-identity-facts">
                <div
                    v-for="fact in card.facts"
                    :key="fact.label"
                    class="profile-identity-fact"
                >
                    <span class="profile-identity-label">
                        {{ fact.label }}
                    </span>

                    <strong class="profile-identity-value">
                        {{ fact.value }}
                    </strong>
                </div>
            </div>
        </div>
    </section>
</template>
