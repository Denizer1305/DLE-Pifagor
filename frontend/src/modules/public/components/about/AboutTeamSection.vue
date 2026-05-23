<script setup lang="ts">
import PublicSectionHead from "@/modules/public/components/shared/PublicSectionHead.vue";
import AboutTeamMemberCard from "@/modules/public/components/about/AboutTeamMemberCard.vue";
import type { AboutTeamContent } from "@/modules/public/data/about-page.data";

interface Props {
    content: AboutTeamContent;
}

defineProps<Props>();
</script>

<template>
    <section
        id="team"
        class="team-section section"
    >
        <div class="container">
            <PublicSectionHead
                :label="content.label"
                :title="content.title"
                :description="content.description"
            />

            <div class="team-shell fade-in">
                <div class="team-layout">
                    <div class="team-intro-card">
                        <div class="team-intro-top">
                            <div class="team-kicker">
                                {{ content.intro.kicker }}
                            </div>

                            <h3 class="team-intro-title">
                                {{ content.intro.title }}
                            </h3>

                            <p class="team-intro-text">
                                {{ content.intro.text }}
                            </p>
                        </div>

                        <div class="team-intro-stats">
                            <div
                                v-for="stat in content.intro.stats"
                                :key="stat.value"
                                class="team-intro-stat"
                            >
                                <strong>{{ stat.value }}</strong>
                                <span>{{ stat.text }}</span>
                            </div>
                        </div>
                    </div>

                    <div class="team-grid">
                        <AboutTeamMemberCard
                            v-for="member in content.members"
                            :key="member.name"
                            :member="member"
                        />
                    </div>
                </div>
            </div>
        </div>
    </section>
</template>
