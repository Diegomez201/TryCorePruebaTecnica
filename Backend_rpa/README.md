# Backend RPA - Prueba Técnica 

Este proyecto implementa el Backend de la prueba, creando una API REST en Flask para la gestión de empresas y estados de procesamiento almacenandola en SQLlite

---

# Propiedades o carcteriticas

La API expone dos endpoints principales para su funcionamiento que son 

1. POST /process-data
   - Recibe un JSON con los datos de una empresa NIT y nombre adicional proporciona un Id con identity y un estado.  
   - Valida y almacena la información en la base de datos de sqllite.  
   - Devuelve el codigo '201' si la empresa fue registrada corrde manera exitosaectamente.  

   por ejemplo para crear una empresa en la base de datos  se tiene como ejemplo el siguiente Script probado en Postman:
   
   {
     "nit": "12345",
     "nombre": "Empresa de Prueba"
   }

2. POST /update-status

Recibe un JSON con el NIT de una empresa y el estado de la transacción (PENDIENTE, PROCESADO, ERROR).

   - Actualiza el estado en la base de datos.
   - Devuelve 200 si la actualización fue exitosa.

por ejemplo se va a actualizar el estado con el Nit de la empresa creada anteriormente desde postman

   {
     "nit": "12345",
     "estado": "PROCESADO"
   }

3. GET /

Para comprobar que la Api esta arriba  o esta corriendo de manera correcta desde postman se puede establecer el metodo GET/ o Abrir la Url desde un Navegador y debe devolver:

{
  "message": "API RPA funcionando"
}


# Autor
Diego Alejandro Gómez Miranda
Prueba Técnica – Desarrollador RPA
