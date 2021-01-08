import pytest
import AQT
import os
import json


class TestBase:
    pass


class TestJsonAPI(TestBase):
	FRAMERATES = [5, 10, 15, 20, 25, 30]
	WB_MODES = ['AUTO', 'CLOUDY', 'FIXED', 'FLUORESCENT', 'HORIZON', 'INCANDESCENT', 'SHADE', 'SUNLIGHT', 'TUNGSTEN']	
	QUALITY_MODES = ['low', 'medium', 'high']
	AF_ALGORITHMS = ['standard', 'expert']

    CAM_ENTITIES = ['analog_gain', 
                'auto_analog_gain_enabled', 
                'auto_digital_gain_enabled', 
                'auto_exposure_enabled', 
                'auto_focus_gain_limit', 
                'auto_ir_filter_enabled', 
                'auto_model_generation_enabled', 
                'auto_model_generation_interval_seconds', 
                'auto_night_mode_disable_threshold', 
                'auto_night_mode_enable_threshold', 
                'auto_night_mode_enabled', 
                'auto_whitebalance', 
                'auto_whitebalance_interval_seconds', 
                'autofocus_algorithm', 
                'compression_quality_modes', 
                'data_routing_policy', 
                'day_mode_FPS', 
                'day_mode_denoising', 
                'day_mode_saturation', 
                'day_mode_sharpening', 
                'day_mode_whitebalance', 
                'denoising', 
                'digital_gain', 
                'exposure_absolute', 
                'exposure_time_milliseconds', 
                'focus_status', 
                'framerate', 
                'gain_absolute', 
                'host', 
                'id', 
                'ir_filter', 
                'kernel', 
                'mcam_state', 
                'mcams_connected', 
                'mcams_expected', 
                'microcameras', 
                'model', 
                'modelGen', 
                'model_generator_found', 
                'night_mode_FPS', 
                'night_mode_denoising', 
                'night_mode_saturation', 
                'night_mode_sharpening', 
                'night_mode_whitebalance', 
                'operating_mode', 
                'quality', 
                'saturation', 
                'serial_number', 
                'sharpening', 
                'software', 
                'state', 
                'supported_autofocus_algorithms', 
                'supported_framerates', 
                'supported_whitebalance_modes', 
                'system_auto_enabled', 
                'system_auto_interval', 
                'whitebalance_mode']

    DR_ENTITIES = ['description', 
			    'global_database', 
			    'host', 
			    'id', 
			    'kernel', 
			    'local_database', 
			    'num_data_receivers', 
			    'parameters', 
			    'per_receiver_connection_limit', 
			    'software', 
			    'state', 
			    'storage_paths', 
			    'type']

    RENDER_ENTITIES = ['GPU_list', 
			    'description', 
			    'host', 'id', 
			    'kernel', 
			    'maximum_render_streams', 
			    'parameters', 
			    'render_streams', 
			    'software', 
			    'state', 
			    'type']


    @pytest.fixture(autouse=True)
    def create_api_objs(self):
        self.api = AQT.AquetiAPI()
        self.cams = [cam.Name() for cam in self.api.GetAvailableCameras()]
        self.cam_params = json.loads(self.api.GetDetailedStatus(self.cams[0]))
        self.rs = [r.Name() for r in self.api.GetAvailableRenderers()]
        self.render_params = json.loads(self.api.GetDetailedStatus(self.rs[0]))
        self.drs = [dr.Name() for dr in self.api.GetAvailableDataRouters()]
        self.dr_params = json.loads(self.api.GetDetailedStatus(self.drs[0]))

    # CAMERA

    def test_cam_entities(self):
        assert set(self.CAM_ENTITIES) == set(self.cam_params.keys())

    def test_cam_analog_gain_imx274(self):
    	assert 0 <= self.cam_params['analog_gain'] <= 22

    def test_cam_auto_analog_gain_enabled(self):
    	assert isinstance(self.cam_params['auto_analog_gain_enabled'], bool)

    def test_cam_auto_digital_gain_enabled(self):
    	assert isinstance(self.cam_params['auto_digital_gain_enabled'], bool)

    def test_cam_auto_exposure_enabled(self):
    	assert isinstance(self.cam_params['auto_exposure_enabled'], bool)

    def test_cam_auto_focus_gain_limit(self):
    	assert self.cam_params['auto_focus_gain_limit'] == 5

    def test_cam_auto_ir_filter_enabled(self):
    	assert self.cam_params['auto_focus_gain_limit']

    def test_cam_auto_model_generation_enabled(self):
    	assert self.cam_params['auto_model_generation_enabled']

    def test_cam_auto_model_generation_interval_seconds(self):
    	assert self.cam_params['auto_model_generation_interval_seconds'] == 0

    def test_cam_auto_night_mode_disable_threshold(self):
    	assert self.cam_params['auto_night_mode_disable_threshold'] == 5

    def test_cam_auto_night_mode_enable_threshold(self):
    	assert 0 <= self.cam_params['auto_night_mode_enable_threshold'] <= 22

    def test_cam_auto_night_mode_enabled(self):
    	assert isinstance(self.cam_params['auto_night_mode_enabled'], bool)

    def test_cam_auto_whitebalance(self):
    	assert isinstance(self.cam_params['auto_whitebalance'], bool)

    def test_cam_auto_whitebalance_interval_seconds(self):
    	assert self.cam_params['auto_whitebalance_interval_seconds'] > 0

    def test_cam_autofocus_algorithm(self):
    	assert self.cam_params['autofocus_algorithm'] in self.AF_ALGORITHMS

    def test_cam_compression_quality_modes(self):
    	assert set(self.cam_params['compression_quality_modes']) == set(self.QUALITY_MODES)

    def test_cam_data_routing_policy(self):
    	assert self.cam_params['data_routing_policy'] == ''

    def test_cam_day_mode_FPS(self):
    	assert self.cam_params['day_mode_FPS'] in self.FRAMERATES

    def test_cam_day_mode_denoising(self):
    	assert 0 <= self.cam_params['day_mode_denoising'] <= 1

    def test_cam_day_mode_saturation(self):
    	assert 0 <= self.cam_params['day_mode_saturation'] <= 1

    def test_cam_day_mode_sharpening(self):
    	assert -1 <= self.cam_params['day_mode_sharpening'] <= 1

    def test_cam_day_mode_whitebalance(self):
    	assert self.cam_params['day_mode_whitebalance'] in ['AUTO']

    def test_cam_denoising(self):
    	assert 0 <= self.cam_params['denoising'] <= 1

   	def test_cam_digital_gain(self):
    	assert 1 <= self.cam_params['digital_gain'] <= 256

    def test_cam_exposure_absolute(self):
    	assert not self.cam_params['exposure_absolute']

    def test_cam_exposure_time_milliseconds(self):
    	assert 0 <= self.cam_params['exposure_time_milliseconds'] <= (1000 / self.cam_params['framerate'])

    def test_cam_focus_status(self):
    	assert self.cam_params['focus_status'] in ['IDLE']

    def test_cam_framerate(self):
    	assert self.cam_params['framerate'] in self.FRAMERATES

    def test_cam_gain_absolute(self):
    	assert self.cam_params['gain_absolute']

    def test_cam_host(self):
    	assert self.cam_params['host'] != ''

    def test_cam_id(self):
    	assert self.cam_params['id'] != ''

    def test_cam_ir_filter(self):
    	assert isinstance(self.cam_params['ir_filter'], bool)

    def test_cam_kernel(self):
    	assert self.cam_params['kernel'] != ''

   	def test_cam_mcam_state(self):
   		assert all('CONNECTED' in row for row in self.cam_params['mcam_state'])

    # 'XX00000000000000001201':'CONNECTED',
    # 'XX00000000000000001202':'CONNECTED',
    # 'XX00000000000000001203':'CONNECTED',

   	def test_cam_mcams_connected(self):
   		assert 0 <= len(self.cam_params['mcams_connected']) <= len(self.cam_params['microcameras'])

    def test_cam_mcams_expected(self):
   		assert len(self.cam_params['mcams_expected']) == len(self.cam_params['microcameras'])  

   	# 'XX00000000000000001201',
    # 'XX00000000000000012010',
    # 'XX00000000000000012011',

    def test_cam_microcameras(self):
   		assert len(self.cam_params['microcameras']) > 0

   	def test_cam_model(self):
   		assert self.cam_params['model'] != ''

   	def test_cam_modelGen(self):
   		if not self.cam_params['modelGen']['inProgress']:
   			assert self.cam_params['modelGen']['currentStep'] == 0
   			assert self.cam_params['modelGen']['databaseConnected']
   			assert self.cam_params['modelGen']['maxStep'] == 4
   			assert self.cam_params['modelGen']['statusText'] == 'idle'

   	def test_cam_model_generator_found(self):
   		assert self.cam_params['model_generator_found']

   	def test_cam_night_mode_FPS(self):
   		assert self.cam_params['night_mode_FPS'] in self.FRAMERATES

    def test_cam_night_mode_denoising(self):
    	assert 0 <= self.cam_params['night_mode_denoising'] <= 1

    def test_cam_night_mode_saturation(self):
    	assert 0 <= self.cam_params['night_mode_saturation'] <= 1

    def test_cam_night_mode_sharpening(self):
    	assert -1 <= self.cam_params['night_mode_sharpening'] <= 1

    def test_cam_night_mode_whitebalance(self):
    	assert self.cam_params['night_mode_whitebalance'] in ['AUTO']

    def test_cam_operating_mode(self):
    	assert isinstance(self.cam_params['operating_mode'], dict)
    	assert self.cam_params['operating_mode']['compression'] in [1, 2, 3]
    	assert self.cam_params['operating_mode']['framerate'] in self.FRAMERATES
    	assert self.cam_params['operating_mode']['tiling_policy'] in list(range(5))

    def test_cam_quality(self):
    	assert set(self.cam_params['quality']) == set(self.QUALITY_MODES)

    def test_cam_saturation(self):
    	assert 0 <= self.cam_params['saturation'] <= 1

    def test_cam_serial_number(self):
    	assert self.cam_params['serial_number'] == '666'

    def test_cam_sharpening(self):
    	assert -1 <= self.cam_params['sharpening'] <= 1

    def test_cam_software(self):
    	assert self.cam_params['software'] != ''

    def test_cam_state(self):
    	assert isinstance(self.cam_params['state'], dict)
    	assert self.cam_params['state']['All Mcams Connected']
    	assert self.cam_params['state']['Database Connection']
    	assert self.cam_params['state']['generalHealth']

    def test_cam_supported_autofocus_algorithms(self):
    	assert self.cam_params['supported_autofocus_algorithms'] == self.AF_ALGORITHMS

    def test_cam_supported_framerates(self):
    	assert self.cam_params['supported_framerates'] == self.FRAMERATES

    def test_cam_supported_whitebalance_modes(self):
    	assert self.cam_params['supported_whitebalance_modes'] == self.WB_MODES

    def test_cam_system_auto_enabled(self):
    	assert isinstance(self.cam_params['system_auto_enabled'], bool)

    def test_cam_system_auto_interval(self):
    	assert self.cam_params['system_auto_interval'] > 0

    def test_cam_whitebalance_mode(self):
    	assert self.cam_params['whitebalance_mode'] in self.WB_MODES

    # DATA ROUTER

    def test_dr_entities(self):
        assert set(self.DR_ENTITIES) == set(self.dr_params.keys())

    def test_dr_description(self):
    	assert self.dr_params['description'] == 'An Aqueti data server'

    def test_dr_global_database(self):
    	assert isinstance(self.dr_params['global_database'], dict)

    	assert self.dr_params['global_database']['name'] != ''
    	assert self.dr_params['global_database']['uri'] != ''

    def test_dr_host(self):
    	uuid_path = '/etc/aqueti/guid'
		with open(uuid_path, "r", encoding="utf-8") as f:
			uuid = f.read().strip()
		
		assert self.dr_params['host'] == uuid

    def test_dr_id(self):
    	assert self.dr_params['id'] != ''

    def test_dr_kernel(self):
    	assert self.dr_params['kernel'] != ''

    def test_dr_kernel(self):
    	assert isinstance(self.dr_params['local_database'])

    	assert self.dr_params['local_database']['name'] != ''
    	assert self.dr_params['local_database']['uri'] != ''

    def test_dr_kernel(self):
    	assert self.dr_params['num_data_receivers'] > 0

    def test_dr_parameters(self):
    	params = self.dr_params['parameters']
    	assert set(params.keys()) == set(['blockSize', 'blocksPerContainer', 'cacheSize', 'garbageCollectionInterval', 'garbageCollectionThreshold', 'maxDiskUsage', 'maxStorageThreads'])

    	assert params['blockSize'] > 0
    	assert params['blocksPerContainer'] > 0
    	assert params['cacheSize'] > 0
    	assert params['garbageCollectionInterval'] >= 0    	
    	assert 0 <= params['garbageCollectionThreshold'] <= 1
    	assert 0 <= params['maxDiskUsage'] <= 1
    	assert params['maxStorageThreads'] > 0

    def test_dr_per_receiver_connection_limit(self):
    	assert self.dr_params['per_receiver_connection_limit'] > 0 

    def test_dr_software(self):
    	assert self.dr_params['software'] != ''

    def test_dr_state(self):
    	assert isinstance(self.dr_params['state'], dict)

		assert self.dr_params['state']['Database Connection'] in ['OK', 'ERROR']
		assert self.dr_params['state']['Storage Space Available'] in ['OK', 'ERROR']
		assert self.dr_params['state']['Valid Storage Paths'] in ['OK', 'ERROR']
		assert self.dr_params['state']['generalHealth'] in ['OK', 'ERROR']

    def test_dr_storage_paths(self):
    	assert isinstance(self.dr_params['storage_paths'], dict)

    	assert dr_params['storage_paths']['available_bytes'] >= 0
    	assert dr_params['storage_paths']['free_bytes'] >= 0
    	assert dr_params['storage_paths']['path'] != ''
    	assert dr_params['storage_paths']['total_bytes'] > 0

    def test_dr_type(self):
    	assert dr_params['type'] == 'Coeus'

    # RENDER

    def test_render_entities(self):
        assert set(self.RENDER_ENTITIES) == set(self.render_params.keys())

    def test_render_GPU_list(self):
        assert isinstance(self.render_params['GPU_list'], list)
        for d in self.render_params['GPU_list']:
	        assert isinstance(d['compatible'], bool)
	        assert d['index'] >= 0
	        assert d['render_stream_count'] >= 0
	        assert d['type'] != ''

	def test_render_description(self):
		assert self.render_params['description'] == 'An Aqueti render server'

	def test_render_host(self):
		uuid_path = '/etc/aqueti/guid'
		with open(uuid_path, "r", encoding="utf-8") as f:
			uuid = f.read().strip()
		
		assert self.render_params['host'] == uuid

	def test_render_id(self):
		assert self.render_params['id'] != ''

	def test_render_kernel(self):
		assert self.render_params['kernel'] != ''

	def test_render_maximum_render_streams(self):
		assert self.render_params['maximum_render_streams'] > 0

	def test_render_parameters(self):
		e_params = set(['backgroundColor', 'maxPixelsDecompressedPerSec', 'numGPUBuffers', 'numH26XDecompressors', 'numJpegDecompressors', 'numTimesInCpuCache', 'prefetchQueueSize', 'streamsPerGPU', 'tightPrefetch'])

		params = self.render_params['parameters']
		assert set(params.keys()) == e_params

		bgcolor = params['backgroundColor']
		assert isinstance(gbcolor, dict)

		assert bgcolor['blue'] == 0
		assert bgcolor['green'] == 0
		assert bgcolor['red'] == 0

		assert params['maxPixelsDecompressedPerSec'] == 1e+38
		assert params['numGPUBuffers'] > 0
		assert params['numH26XDecompressors'] > 0
		assert params['numJpegDecompressors'] > 0
		assert params['numTimesInCpuCache'] > 0
		assert params['prefetchQueueSize'] > 0
		assert params['streamsPerGPU'] > 0
		assert isinstance(params['tightPrefetch'], bool)

	def test_render_render_streams(self):
		assert isinstance(self.render_params['render_streams'], list)

	def test_render_software(self):
		assert self.render_params['software'] != ''

	def test_render_state(self):
		assert isinstance(self.render_params['state'], dict)

		assert self.render_params['state']['Compatible GPU'] in ['OK', 'ERROR']
		assert self.render_params['state']['Display Environment'] in ['OK', 'ERROR']
		assert self.render_params['state']['Forcing Gpu Compatibility'] in ['OK', 'ERROR']
		assert self.render_params['state']['Render Stream Available'] in ['OK', 'ERROR']
		assert self.render_params['state']['generalHealth'] in ['OK', 'ERROR']

	def test_render_type(self):
		assert self.render_params['type'] == 'Hyperion'

	# ALL

	def test_all_software(self):
		pass #assert cam_params['software'] == render_params['software'] == dr_params['software']
