from odoo import models, fields, api, exceptions

class CrmTeam(models.Model):
    
    ######################
    # Private attributes #
    ######################
    _inherit = "crm.team"

    ###################
    # Default methods #
    ###################

    ######################
    # Fields declaration #
    ######################
    stage_stats = fields.Html(string="Stats",
        compute="_compute_stage_stats")
    
    stage_ids = fields.One2many(string="Stages",
        comodel_name="crm.stage",
        inverse_name="team_id")
    
    ##############################
    # Compute and search methods #
    ##############################
    @api.multi
    def _compute_stage_stats(self):
        for team in self:
            total_cw = 0
            total_cb = 0
            total_co = 0
            total_tw = 0
            total_tb = 0
            total_to = 0
            
            table_header = """ 
                <table class="table table-bordered table-sm mt-2">
                    <tbody>
                        <tr align='center'>
                            <th align='left'>STAGE</td>
                            <th style='color:green;'>CW</th>
                            <th style='color:red;'>CB</th>
                            <th>CO</th>
                            <th style='color:green;'>TW</th>
                            <th style='color:red;'>TB</th>
                            <th>TO</th>
                        </tr> 
                """
            table_body = ""
            for stage in team.stage_ids:
                table_body += """
                    <tr align='center'>
                        <td align='left'>{}</td>
                        <td style='color:green;'>{}</td>
                        <td style='color:red;'>{}</td>
                        <td>{}</td>
                        <td style='color:green;'>{}</td>
                        <td style='color:red;'>{}</td>
                        <td>{}</td>
                    </tr>
                """.format(stage.name,
                           stage.current_within,
                           stage.current_beyond,
                           stage.current_within + stage.current_beyond,
                           stage.total_within,
                           stage.total_beyond, 
                           stage.total_within + stage.total_beyond)
                
                total_cw += stage.current_within
                total_cb += stage.current_beyond
              
                total_tw += stage.total_within
                total_tb += stage.total_beyond
            
            table_footer = """
                        <tr align='center'>
                            <th></th>
                            <th style='color:green;'>{}</th>
                            <th style='color:red;'>{}</th>
                            <th>{}</th>
                            <th style='color:green;'>{}</th>
                            <th style='color:red;'>{}</th>
                            <th>{}</th
                        </tr>
                    </tbody>
                </table> 
            """.format(total_cw,
                       total_cb,
                       total_cw + total_cb,
                       total_tw,
                       total_tb,
                       total_tw + total_tb)
            
            team.stage_stats = table_header + table_body + table_footer
        
        
    ############################
    # Constrains and onchanges #
    ############################

    #########################
    # CRUD method overrides #
    #########################


    ##################
    # Action methods #
    ##################

    ####################
    # Business methods #
    ####################