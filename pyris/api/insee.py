from flask_restplus import Namespace, Resource, fields

from pyris.api import extract


api = Namespace('insee', description='Some stats from INSEE for each IRIS')

population_parser = api.parser()
population_parser.add_argument("by", required=True, location='args',
                               help="By 'sex' or 'age'")



@api.route('/')
class InseeData(Resource):
    @api.doc('INSEE data list')
    def get(self):
        return ['population', 'activite', 'logement',
                'menage', 'formation']


@api.route('/population/<string:code>')
class IrisPopulation(Resource):
    @api.doc("get the population for an IRIS")
    def get(self, code):
        if len(code) != 9:
            api.abort(400, "IRIS code is malformed (9 digits)")
        rset = extract.get_iris_population(code)
        if not rset:
            api.abort(404, "IRIS code '{}' not found".format(code))
        return rset[0]


@api.route('/population/distribution/<string:code>')
class IrisPopulationDistribution(Resource):
    @api.doc(parser=population_parser,
             description="get population for an IRIS")
    def get(self, code):
        if len(code) != 9:
            api.abort(400, "IRIS code is malformed (9 digits)")
        args = population_parser.parse_args()
        if args['by'] not in ('sex', 'age'):
            api.abort(400, "By query param should be 'sex' or 'age'")
        if args['by'] == 'sex':
            rset = extract.get_iris_population_sex(code)
        if args['by'] == 'age':
            rset = extract.get_iris_population_age(code)
        if not rset:
            api.abort(404, "IRIS code '{}' not found".format(code))
        return rset[0]
