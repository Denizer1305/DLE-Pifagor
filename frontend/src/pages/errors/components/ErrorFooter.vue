<script setup lang="ts">
defineProps<{
    text: string;
    email: string;
    phone: string;
}>();
</script>

<template>
    <footer class="error-footer">
        <p>
            <span>{{ text }}</span>
            <span aria-hidden="true">•</span>
            <a :href="`mailto:${email}`">{{ email }}</a>
            <span aria-hidden="true">•</span>
            <span>Техническая поддержка: {{ phone }}</span>
        </p>
    </footer>
</template>
