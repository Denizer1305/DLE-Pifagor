<script setup lang="ts">
import OrganizationActionMenu from "../shared/OrganizationActionMenu.vue";
import OrganizationStatusBadge from "../shared/OrganizationStatusBadge.vue";

import type {
    JoinRequestListItemView,
    OrganizationTableAction,
    OrganizationTableActionKey,
    OrganizationTableColumn,
} from "../../types";

interface Props {
    items: JoinRequestListItemView[];
    columns: OrganizationTableColumn[];
    actions: OrganizationTableAction[];
    disabledActions?: Partial<Record<number, OrganizationTableActionKey[]>>;
}

interface Emits {
    (event: "select", item: JoinRequestListItemView): void;
    (
        event: "action",
        payload: {
            actionKey: OrganizationTableActionKey;
            item: JoinRequestListItemView;
        },
    ): void;
}

const props = withDefaults(defineProps<Props>(), {
    disabledActions: () => ({}),
});

defineEmits<Emits>();

function getDisabledActions(
    item: JoinRequestListItemView,
): OrganizationTableActionKey[] {
    const disabledActions = props.disabledActions[item.id] ?? [];

    if (item.canReview) {
        return disabledActions;
    }

    return [
        ...disabledActions,
        "approve",
        "reject",
    ];
}
</script>

<template>
    <section class="org-table">
        <div class="org-table__scroll">
            <table class="org-table__table">
                <thead class="org-table__head">
                    <tr class="org-table__row">
                        <th
                            v-for="column in columns"
                            :key="column.key"
                            class="org-table__cell org-table__cell--head"
                            :class="{
                                'org-table__cell--actions': column.key === 'actions',
                                'org-table__cell--compact': column.width,
                            }"
                            :style="{ width: column.width }"
                        >
                            {{ column.label }}
                        </th>
                    </tr>
                </thead>

                <tbody class="org-table__body">
                    <tr
                        v-for="item in items"
                        :key="item.id"
                        class="org-table__row"
                    >
                        <td
                            class="org-table__cell"
                            data-label="Пользователь"
                        >
                            <button
                                class="org-table__entity"
                                type="button"
                                @click="$emit('select', item)"
                            >
                                <span class="org-table__avatar">
                                    {{ item.userName.slice(0, 2).toUpperCase() }}
                                </span>

                                <span class="org-table__entity-content">
                                    <span class="org-table__title">
                                        {{ item.userName }}
                                    </span>

                                    <span class="org-table__subtitle">
                                        {{ item.userContacts }}
                                    </span>

                                    <span class="org-table__meta">
                                        <span
                                            v-for="metaItem in item.meta"
                                            :key="metaItem"
                                            class="org-table__meta-item"
                                        >
                                            {{ metaItem }}
                                        </span>
                                    </span>
                                </span>
                            </button>
                        </td>

                        <td
                            class="org-table__cell"
                            data-label="Тип заявки"
                        >
                            <span class="org-table__title">
                                {{ item.typeLabel }}
                            </span>

                            <span class="org-table__subtitle">
                                Создана: {{ item.createdAtLabel }}
                            </span>
                        </td>

                        <td
                            class="org-table__cell"
                            data-label="Куда"
                        >
                            <span class="org-table__title">
                                {{ item.targetTitle }}
                            </span>

                            <span class="org-table__subtitle">
                                {{ item.message }}
                            </span>
                        </td>

                        <td
                            class="org-table__cell"
                            data-label="Статус"
                        >
                            <OrganizationStatusBadge :status="item.status" />
                        </td>

                        <td
                            class="org-table__cell org-table__cell--actions"
                            data-label="Действия"
                        >
                            <OrganizationActionMenu
                                :actions="actions"
                                :disabled-actions="getDisabledActions(item)"
                                @action="
                                    $emit('action', {
                                        actionKey: $event,
                                        item,
                                    })
                                "
                            />
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </section>
</template>