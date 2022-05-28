import { withAuth, session } from './auth';
import { list, config } from '@keystone-6/core';
import { text,relationship,timestamp,select,password } from '@keystone-6/core/fields';

const lists = {
  User: list({
    fields: {
      name: text({ validation: { isRequired: true } }),
      email: text({ validation: { isRequired: true }, isIndexed: 'unique' }),
      password: password({ validation: { isRequired: true } })
    },
  }),
  jkbb: list({
    fields: {
      account: text({ validation: { isRequired: true } }),
      password: text({ validation: { isRequired: true }}),
      departName: text({ validation: { isRequired: true }}),
      instructorName: text({ validation: { isRequired: true }}),
      address: text({ validation: { isRequired: true }}),
      latitude: text({ validation: { isRequired: true }}),
      longitude: text({ validation: { isRequired: true }}),
      permanentAddress: text({ validation: { isRequired: true }}),
      isStayLocal: select({
        options: [
          { label: 'yes', value: '1' },
          { label: 'no', value: '0' },
        ],
        defaultValue: '1',
        ui: { displayMode: 'segmented-control' },
      }),
      isStaySchool: select({
        options: [
          { label: 'yes', value: '1' },
          { label: 'no', value: '0' },
        ],
        defaultValue: '1',
        ui: { displayMode: 'segmented-control' },
      }),
      phone_number: text({ validation: { isRequired: true }}),
      emergencyName: text({ validation: { isRequired: true }}),
      emergencyPhone: text({ validation: { isRequired: true }})
    },
  }),
};

export default withAuth(
  // Using the config function helps typescript guide you to the available options.
  config({
    // the db sets the database provider - we're using sqlite for the fastest startup experience
    db: {
      provider: 'sqlite',
      url: 'file:./keystone.db',
    },
    // This config allows us to set up features of the Admin UI https://keystonejs.com/docs/apis/config#ui
    ui: {
      // For our starter, we check that someone has session data before letting them see the Admin UI.
      isAccessAllowed: (context) => !!context.session?.data,
    },
    lists,
    session,
  })
);
