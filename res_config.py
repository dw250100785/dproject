# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Business Applications
#    Copyright (C) 2004-2012 OpenERP S.A. (<http://openerp.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import fields, osv
from openerp.tools.translate import _
# 配置文件也是存放在数据库表里
#dproject_config_settings

class dproject_configuration(osv.osv_memory):
    _name = 'dproject.config.settings'
    _inherit = 'res.config.settings'
    # 配置项 全部在后面添加  _d
    _columns = {
        'module_project_mrp_d': fields.boolean('Generate tasks from sale orders',
            help ="""This feature automatically creates project tasks from service products in sale orders.
                More precisely, tasks are created for procurement lines with product of type 'Service',
                procurement method 'Make to Order', and supply method 'Manufacture'.
                This installs the module project_mrp."""),


        'module_pad_d': fields.boolean("Use integrated collaborative note pads on task",
            help="""Lets the company customize which Pad installation should be used to link to new pads
                (by default, http://ietherpad.com/).
                This installs the module pad."""),


        'module_project_timesheet_d': fields.boolean("Record timesheet lines per tasks",
            help="""This allows you to transfer the entries under tasks defined for Project Management to
                the timesheet line entries for particular date and user, with the effect of creating,
                editing and deleting either ways.
                This installs the module project_timesheet."""),


        'module_project_long_term_d': fields.boolean("Manage resources planning on gantt view",
            help="""A long term project management module that tracks planning, scheduling, and resource allocation.
                This installs the module project_long_term."""),


        'module_dproject_issue_d': fields.boolean("Track issues and bugs",
            help="""Provides management of issues/bugs in projects.
                This installs the module project_issue."""),


        'time_unit_d': fields.many2one('product.uom', 'Working time unit', required=True,
            help="""This will set the unit of measure used in projects and tasks."""),


        'module_project_issue_sheet_d': fields.boolean("Invoice working time on issues",
            help="""Provides timesheet support for the issues/bugs management in project.
                This installs the module project_issue_sheet."""),

        'group_tasks_work_on_tasks_d': fields.boolean("Log work activities on tasks",
            implied_group='project.group_tasks_work_on_tasks',
            help="Allows you to compute work on tasks."),


        'group_time_work_estimation_tasks_d': fields.boolean("Manage time estimation on tasks",
            implied_group='project.group_time_work_estimation_tasks',
            help="Allows you to compute Time Estimation on tasks."),

        'group_manage_delegation_task_d': fields.boolean("Allow task delegation",
            implied_group='project.group_delegate_task',
            help="Allows you to delegate tasks to other users."),
    }

    def get_default_time_unit(self, cr, uid, fields, context=None):
        user = self.pool.get('res.users').browse(cr, uid, uid, context=context)
        return {'time_unit_d': user.company_id.project_time_mode_id.id}

    def set_time_unit(self, cr, uid, ids, context=None):
        config = self.browse(cr, uid, ids[0], context)
        user = self.pool.get('res.users').browse(cr, uid, uid, context)
        user.company_id.write({'dproject_time_mode_id': config.time_unit.id})

    def onchange_time_estimation_project_timesheet(self, cr, uid, ids, group_time_work_estimation_tasks, module_project_timesheet):
        if group_time_work_estimation_tasks or module_project_timesheet:
            return {'value': {'group_tasks_work_on_tasks_d': True}}
        return {}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
