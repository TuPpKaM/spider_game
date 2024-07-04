import json


class ClassRegistry:
    _registry = {}

    @classmethod
    def register_class(cls, class_ref):
        cls._registry[class_ref.__name__] = class_ref

    @classmethod
    def get_class(cls, class_name):
        return cls._registry[class_name]


class Registry:
    _registry = []

    @classmethod
    def register_instance(cls, instance):
        cls._registry.append(instance)

    @classmethod
    def remove_instances_of_class(cls, class_type):
        cls._registry = [instance for instance in cls._registry if not isinstance(instance, class_type)]

    @classmethod
    def to_dict(cls):
        return [instance.to_dict() for instance in cls._registry]

    @classmethod
    def save_to_file(cls, filename):
        with open(filename, 'w') as f:
            f.truncate(0)
            json.dump(cls.to_dict(), f)
    
    @classmethod
    def from_dict(cls, data, isometric_conversions, animation_manager, group, egg_group):
        for item in data:
            class_name = item.pop('class_name')
            class_ref = ClassRegistry.get_class(class_name) #class_ref = globals()[class_name]
            #TODO:: cleanup if else
            if class_name == 'Spiderling':
                class_ref.from_dict(item, isometric_conversions, animation_manager, group)
            elif class_name == 'RedSpider':
                class_ref.from_dict(item, isometric_conversions, animation_manager, group, egg_group)
            else:
                raise ValueError(f"Unknown class name: {class_name}")
            
            #cls.register_instance(instance) TODO::

    @classmethod
    def load_from_file(cls, filename, isometric_conversions, animation_manager, group, egg_group): # TODO:: args? kwargs?
        with open(filename, 'r') as f:
            data = json.load(f)
            cls._registry.clear()
            cls.from_dict(data, isometric_conversions, animation_manager, group, egg_group)
