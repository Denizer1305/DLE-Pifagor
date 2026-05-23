<script setup lang="ts">
import { RouterLink } from "vue-router";

import ProfileEducationCard from "@/modules/profile/components/ProfileEducationCard.vue";
import type { ProfileRoleSectionModel } from "@/modules/profile/types/profile.types";

interface Props {
    section: ProfileRoleSectionModel;
}

defineProps<Props>();
</script>

<template>
    <section class="teacher-profile-role fade-in visible">
        <div class="teacher-profile-role-head">
            <div>
                <div class="teacher-profile-role-topline">
                    <i class="fas fa-user-shield"></i>
                    Роль пользователя
                </div>

                <h2 class="teacher-profile-role-title">
                    {{ section.title }}
                </h2>

                <p class="teacher-profile-role-text">
                    {{ section.text }}
                </p>
            </div>

            <RouterLink
                class="teacher-profile-role-action"
                :to="{ name: 'profile-edit' }"
            >
                <i class="fas fa-pen-to-square"></i>
                Редактировать профиль
            </RouterLink>
        </div>

        <div class="teacher-profile-role-grid">
            <article class="teacher-profile-role-card teacher-profile-role-card-main">
                <div class="teacher-role-card-top">
                    <div class="teacher-role-card-icon">
                        <i class="fas fa-briefcase"></i>
                    </div>

                    <div>
                        <h3 class="teacher-role-card-title">
                            Ролевая информация
                        </h3>

                        <p class="teacher-role-card-text">
                            Базовые данные, связанные с активной ролью пользователя внутри платформы.
                        </p>
                    </div>
                </div>

                <div class="teacher-role-facts">
                    <div
                        v-for="fact in section.facts"
                        :key="fact.label"
                        class="teacher-role-fact"
                    >
                        <span class="teacher-role-fact-label">
                            {{ fact.label }}
                        </span>

                        <strong class="teacher-role-fact-value">
                            {{ fact.value }}
                        </strong>
                    </div>
                </div>
            </article>

            <article
                v-if="section.tags.length"
                class="teacher-profile-role-card"
            >
                <div class="teacher-role-card-top">
                    <div class="teacher-role-card-icon">
                        <i class="fas fa-book-open-reader"></i>
                    </div>

                    <div>
                        <h3 class="teacher-role-card-title">
                            Направления
                        </h3>

                        <p class="teacher-role-card-text">
                            Предметные или профессиональные направления, связанные с ролью пользователя.
                        </p>
                    </div>
                </div>

                <div class="teacher-role-tags">
                    <span
                        v-for="tag in section.tags"
                        :key="tag"
                        class="teacher-role-tag"
                    >
                        {{ tag }}
                    </span>
                </div>
            </article>

            <article
                v-if="section.groups.length"
                class="teacher-profile-role-card"
            >
                <div class="teacher-role-card-top">
                    <div class="teacher-role-card-icon">
                        <i class="fas fa-users"></i>
                    </div>

                    <div>
                        <h3 class="teacher-role-card-title">
                            Группы и связи
                        </h3>

                        <p class="teacher-role-card-text">
                            Учебные группы, связанные пользователи или рабочие связи профиля.
                        </p>
                    </div>
                </div>

                <div class="teacher-role-group-list">
                    <div
                        v-for="group in section.groups"
                        :key="group.title"
                        class="teacher-role-group-item"
                    >
                        <strong>{{ group.title }}</strong>
                        <span>{{ group.text }}</span>
                    </div>
                </div>
            </article>

            <ProfileEducationCard
                v-if="section.education.length"
                :items="section.education"
            />
        </div>
    </section>
</template>