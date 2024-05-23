<script setup>
import TimetableWrapper from "./TimetableWrapper.vue";
</script>
<script>
export default {
  name: "Timetable",
};
</script>

<template>
  <timetable-wrapper>
    <template #default="{ selected }">
      <calendar-with-controls
        :calendar-feeds="[{ name: 'lesson' }, { name: 'supervision' }]"
        :params="{ type: selected.type, id: selected.objId }"
      />
    </template>
  </timetable-wrapper>
</template>
