<script setup lang="ts">
interface ProfileEducationItem {
    title: string;
    text: string;
}

interface Props {
    items: ProfileEducationItem[];
}

defineProps<Props>();
</script>

<template>
    <article class="teacher-profile-role-card teacher-profile-role-card-wide">
        <div class="teacher-role-card-top">
            <div class="teacher-role-card-icon">
                <i class="fas fa-graduation-cap"></i>
            </div>

            <div>
                <h3 class="teacher-role-card-title">
                    Образование и квалификация
                </h3>

                <p class="teacher-role-card-text">
                    Информация об образовании, квалификации, опыте и профессиональных достижениях.
                </p>
            </div>
        </div>

        <div class="teacher-role-education-list">
            <div
                v-for="item in items"
                :key="item.title"
                class="teacher-role-education-item"
            >
                <strong>{{ item.title }}</strong>
                <span>{{ item.text }}</span>
            </div>
        </div>
    </article>
</template>