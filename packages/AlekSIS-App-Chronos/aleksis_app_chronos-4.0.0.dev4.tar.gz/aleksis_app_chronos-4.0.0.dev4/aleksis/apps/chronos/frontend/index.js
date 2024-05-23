import { hasPersonValidator } from "aleksis.core/routeValidators";
import Timetable from "./components/Timetable.vue";

export default {
  meta: {
    inMenu: true,
    titleKey: "chronos.menu_title",
    icon: "mdi-school-outline",
    iconActive: "mdi-school",
    validators: [hasPersonValidator],
  },
  children: [
    {
      path: "timetable/",
      component: Timetable,
      name: "chronos.timetable",
      meta: {
        inMenu: true,
        titleKey: "chronos.timetable.menu_title",
        toolbarTitle: "chronos.timetable.menu_title",
        icon: "mdi-grid",
        permission: "chronos.view_timetable_overview_rule",
        fullWidth: true,
      },
    },
    {
      path: "timetable/:type/:id/",
      component: Timetable,
      name: "chronos.timetableWithId",
      meta: {
        permission: "chronos.view_timetable_overview_rule",
        fullWidth: true,
      },
    },
  ],
};
