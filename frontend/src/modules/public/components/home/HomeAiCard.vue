<script setup lang="ts">
interface AiLogicItem {
    title: string;
    text: string;
}

interface AiCard {
    variant?: string;
    label: string;
    icon: string;
    title: string;
    text: string;
    points?: string[];
    logic?: AiLogicItem[];
    quote?: string;
    quoteSub?: string;
}

interface Props {
    card: AiCard;
}

defineProps<Props>();
</script>

<template>
    <article
        class="ai-card fade-in"
        :class="card.variant"
    >
        <div class="ai-card-inner">
            <div class="ai-pill">
                <i :class="card.icon"></i>
                {{ card.label }}
            </div>

            <h3 class="ai-card-title">
                {{ card.title }}
            </h3>

            <p class="ai-card-text">
                {{ card.text }}
            </p>

            <ul
                v-if="card.points?.length"
                class="ai-list"
            >
                <li
                    v-for="point in card.points"
                    :key="point"
                >
                    <span class="ai-list-dot"></span>
                    <span>{{ point }}</span>
                </li>
            </ul>

            <div
                v-if="card.logic?.length"
                class="ai-logic-grid"
            >
                <div
                    v-for="item in card.logic"
                    :key="item.title"
                    class="ai-logic-item"
                >
                    <strong>{{ item.title }}</strong>
                    <span>{{ item.text }}</span>
                </div>
            </div>

            <div
                v-if="card.quote"
                class="ai-quote"
            >
                <div class="ai-quote-text">
                    {{ card.quote }}
                </div>

                <div
                    v-if="card.quoteSub"
                    class="ai-quote-sub"
                >
                    {{ card.quoteSub }}
                </div>
            </div>
        </div>
    </article>
</template>
