<script setup lang="ts">
interface Props {
    icon: string;
    topline: string;
    title: string;
    text: string;
}

defineProps<Props>();
</script>

<template>
    <section class="settings-section fade-in visible">
        <article class="settings-card">
            <div class="settings-card-head">
                <div>
                    <div class="settings-card-topline">
                        <i :class="icon"></i>
                        {{ topline }}
                    </div>

                    <h2 class="settings-card-title">
                        {{ title }}
                    </h2>

                    <p class="settings-card-text">
                        {{ text }}
                    </p>
                </div>

                <slot name="actions"></slot>
            </div>

            <div class="settings-card-body">
                <slot></slot>
            </div>
        </article>
    </section>
</template>
