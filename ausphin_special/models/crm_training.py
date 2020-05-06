from datetime import timedelta

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class CrmTraining(models.Model):
    
    ######################
    # Private attributes #
    ######################
    _inherit = "crm.training"

    ###################
    # Default methods #
    ###################

    ######################
    # Fields declaration #
    ######################
    
    ##############################
    # Compute and search methods #
    ##############################

    ############################
    # Constrains and onchanges #
    ############################
    @api.constrains("interview_date")
    def _check_interview_date(self):
        activity_obj = self.env["mail.activity"]
        res_model_id = self.env.ref("base.model_res_partner").id
        for training in self:
            if not training.lead_id.partner_id:
                raise ValidationError("Failed to create mock interview activity because there is no related contact")
            if training.interview_date:
                user = training.lead_id.user_id
                first_stage = training.lead_id.stage_id.team_id.stage_ids[0]
                for log in training.lead_id.stage_log_ids.filtered(lambda l: l.stage_id.id == first_stage.id):
                    if log.user_id:
                        user = log.user_id
                        break
                date_deadline = (training.interview_date - timedelta(days=1)).date()
                summary = "Mock Interview for " + training.venue_id.name
                timezone = user.partner_id.tz or "UTC"
                self_tz = self.with_context(tz=timezone)
                note = "Actual Interview Schedule: " + \
                       str(fields.Datetime.context_timestamp(self_tz, training.interview_date)) + \
                       " (Timezone=" + timezone + ")"
                partner_id = training.lead_id.partner_id.id
                
                # update existing activity if any
                matched_activity = activity_obj.sudo().search([
                    ("summary","=",summary),
                    ("res_id","=",partner_id),
                    ("res_model_id","=",res_model_id)
                ])
                if matched_activity:
                    matched_activity.write({
                        "date_deadline": date_deadline,
                        "note": note,
                        "user_id": user.id,
                    })
                    continue
                
                # create activity
                activity_obj.create({
                    "activity_type_id": self.env.ref("mail.mail_activity_data_call").id,
                    "summary": summary,
                    "user_id": user.id,
                    "res_id": partner_id,
                    "res_model_id": res_model_id,
                    "date_deadline": date_deadline,
                    "note": note,
                })

    #########################
    # CRUD method overrides #
    #########################

    ##################
    # Action methods #
    ##################

    ####################
    # Business methods #
    ####################